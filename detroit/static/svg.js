const svgns = "http://www.w3.org/2000/svg";
const avoidedAttributes = ["viewBox", "class", "width", "height"];
const fullAvoidedAttributes = ["viewBox", "class", "width", "height", "stroke", "fill"];

// Convenient function to convert a string into integer
function int(string){
  return parseInt(string, 10);
}

// Get attributes names of a svg object and filter them
// given `attributes` argument
function getAttributeNames(svg, attributes = avoidedAttributes){
  return svg.getAttributeNames().filter(name => !(attributes.includes(name)));
}

// Generate a group from svg object
function gFromSVG(svg, lastHeight){
  const boundingRect = svg.getBoundingClientRect();
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  for (const name of getAttributeNames(svg)){g.setAttribute(name, svg.getAttribute(name));}
  g.setAttribute("transform", `translate(0, ${lastHeight})`)
  g.append(...svg.childNodes);
  return g;
}

// Generate a group from svg object included into a span
function gSVGFromSpan(svg){
  const style = window.getComputedStyle(svg);
  const dx = int(style.marginLeft) - int(style.marginRight);
  const dy = int(style.marginTop) - int(style.marginBottom);
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  for (const name of getAttributeNames(svg)){g.setAttribute(name, svg.getAttribute(name));}
  g.setAttribute("transform", `translate(${dx}, ${dy})`)
  g.append(...svg.childNodes);
  return g
}

function gSVGFromRectSVG(svg) {
  const boundingRect = svg.getBoundingClientRect();
  const width = boundingRect.width;
  const height = boundingRect.height;
  const rect = svg.childNodes[0];
  rect.setAttribute("width", width);
  rect.setAttribute("height", height);
  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
  for (const name of getAttributeNames(svg)){g.setAttribute(name, svg.getAttribute(name));}
  g.setAttribute("transform", `translate(${width / 2}, ${-height / 2})`)
  g.append(rect);
  return g
}

// Generate a text from a span
function textFromSpan(string, x, grid, isTitle = false){
  const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  text.setAttribute("transform", `translate(${x}, 0)`)
  if (isTitle){
    const style = window.getComputedStyle(document.body);
    text.setAttribute("dominant-baseline", "middle")
    text.setAttribute("text-anchor", "middle")
    text.setAttribute("x", `${50 / grid}%`);
    text.setAttribute("y", "1%");
    text.setAttribute("fill", style.color);
  } else {
    text.setAttribute("y", "0.32em");
  }
  text.append(string);
  return text;
}

// Generate a group from a span
function gFromSpan(span, spanCount, lastHeight){
  const svg = span.childNodes[0];
  const text = span.childNodes[1];
  const svgBoundingRect = svg.getBoundingClientRect();
  const textBoundingRect = span.getBoundingClientRect();
  const xText = textBoundingRect.width - svgBoundingRect.width;
  const svgChildNodes = Array.from(svg.childNodes);
  const onlyRect = svgChildNodes.length === 1 && svgChildNodes[0].tagName === "rect"

  var style = window.getComputedStyle(span);
  var dx = int(style.marginLeft) - int(style.marginRight);

  const g = document.createElementNS("http://www.w3.org/2000/svg", "g");

  const x = (onlyRect) ? (textBoundingRect.width - dx) * spanCount : textBoundingRect.width + (textBoundingRect.width - dx) * spanCount;
  const y = textBoundingRect.height + lastHeight;
  g.setAttribute("transform", `translate(${x}, ${y})`)
  g.append((onlyRect) ? gSVGFromRectSVG(svg) : gSVGFromSpan(svg));
  g.append(textFromSpan(text, xText, 0, false))
  return g;
}

// Generate a group from an object
function gFromObj(obj, grid = 1, lastHeight = 0, layer = 0){
  var childNodes = [];
  var spanCount = 0;
  var heightForSpan = 0;
  for (const child of obj.childNodes){
    switch(child.tagName){
      case "SPAN":
        var tmpHeight = child.getBoundingClientRect().height;
        childNodes.push(gFromSpan(child, spanCount, heightForSpan));
        spanCount += 1;
        break;
      case "svg":
        var tmpHeight = child.getBoundingClientRect().height;
        childNodes.push(gFromSVG(child, lastHeight));
        break;
      case "STYLE":
        var heightForSpan = lastHeight;
        var tmpHeight = 0;
        break;
      case "DIV":
        var tmpHeight = child.getBoundingClientRect().height;
        childNodes.push(...gFromObj(child, grid, lastHeight, layer + 1));
        break;
      case "FIGURE":
        var tmpHeight = child.getBoundingClientRect().height;
        childNodes.push(...gFromObj(child, grid, lastHeight, layer + 1));
        break;
      case "H2":
        var tmpHeight = child.getBoundingClientRect().height;
        childNodes.push(textFromSpan(child.textContent, 0, grid, true));
        break;
      default:
        var tmpHeight = 0;
        break;
    }
    lastHeight += tmpHeight;
  }
  return childNodes;
}

// Generate a group from a grid (multiple objects)
function gFromGrid(obj, grid){
  var childNodes = [];
  var x = 0;
  var y = 0;
  var currentMaxHeight = 0;
  var maxWidth = 0;
  var maxHeight = 0;
  var index = 0;
  for (const child of obj.childNodes) {
    if (child.tagName === "DIV"){
      var subchild = Array.from(child.childNodes).filter(c => c.tagName === "DIV")[0].childNodes[0];
      var width = (subchild.tagName === "FIGURE") ? subchild.clientWidth : subchild.width.baseVal.value;
      var height = child.getBoundingClientRect().height;
      var currentMaxHeight = (index % grid === 0 && index !== 0) ? height: Math.max(currentMaxHeight, height);
      var x = (index % grid === 0) ? 0 : x + width;
      var y = (index % grid === 0 && index !== 0) ? y + currentMaxHeight : y;
      var maxWidth = Math.max(x, maxWidth);
      var maxHeight = Math.max(y, maxHeight);
      var g = document.createElementNS("http://www.w3.org/2000/svg", "g");
      g.setAttribute("transform", `translate(${x}, ${y})`)
      g.append(...gFromObj(child, grid));
      childNodes.push(g);
      index += 1;
    }
  }
  return [childNodes, maxWidth + width, maxHeight + height];
}

// Generate a new svg from a grid (multiple objects)
function makeSVGfromGrid(div, svg, grid){
  const [g, width, height] = gFromGrid(div, grid);
  const style = window.getComputedStyle(document.body);
  const new_svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  for (const name of getAttributeNames(svg, fullAvoidedAttributes)){new_svg.setAttribute(name, svg.getAttribute(name));}
  new_svg.setAttribute("width", `${width}`);
  new_svg.setAttribute("height", `${height}`);
  new_svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  new_svg.setAttribute("fill", style.color);
  new_svg.append(...g);
  div.remove(...div.childNodes)
  document.body.appendChild(new_svg);
  return new_svg;
}

// Generate a new svg from a div containing a svg object
function makeSVGfromSimple(div, svg){
  const width = svg.getBoundingClientRect().width;
  const height = div.getBoundingClientRect().height;
  const g = gFromObj(div);
  const style = window.getComputedStyle(document.body);
  const new_svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  for (const name of getAttributeNames(svg, fullAvoidedAttributes)){new_svg.setAttribute(name, svg.getAttribute(name));}
  new_svg.setAttribute("width", `${width}`);
  new_svg.setAttribute("height", `${height}`);
  new_svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  new_svg.setAttribute("fill", style.color);
  new_svg.append(...g);
  div.remove(...div.childNodes)
  document.body.appendChild(new_svg);
  return new_svg;
}
