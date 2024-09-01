{{ import_package }}
import { JSDOM } from "jsdom";
import WebSocket from "ws";
import performance from "perf_hooks";
import { transform } from "@observablehq/plot";
const dom = new JSDOM();

var start = performance.performance.now();
let div = dom.window.document.createElement("div");
dom.window.document.body.appendChild(div);
div.id = "myplot";

{% if multiple %}
const ids = Array.from(Array({{code|length}}).keys());
const containers = ids.map(_ => dom.window.document.createElement("div"));
const divs = ids.map(_ => dom.window.document.createElement("div"));
{% if titles %}const h2s = ids.map(_ => dom.window.document.createElement("h2"));
const titles = [{{ titles }}];
for (const [i, h2] of h2s.entries()){
  h2.append(titles[i]);
  containers[i].append(h2);
}{% endif %}
for (const [i, d] of divs.entries()){
  containers[i].append(d);
}
div.append(...containers);
{% endif %}

const avoidedAttributes = ["viewBox", "class", "width", "height"];

// Convenient function to convert a string into integer
function int(string){
  return parseInt(string, 10);
}

function float(string){
  return parseFloat(string);
}

class Tracer {
  constructor(figure) {
    this.fontSize = 10;
    this.svg = this.create("svg");
    let [width, height] = figure.tagName === "svg" ? this.walkIntoSVG(figure) : this.walkInto(figure, this.svg).slice(0, 2);
    const [style, fill, fontFamily] = this.extractReferences(figure);
    if (figure.tagName === "DIV") {
      const h2 = figure.childNodes[0];
      const [text, fontSize] = this.makeH2(h2, width);
      this.svg.childNodes[0].setAttribute("transform", `translate(0, ${fontSize})`);
      this.svg.prepend(text);
      height += fontSize;
    }
    this.svg.setAttribute("width", width);
    this.svg.setAttribute("height", height);
    this.svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    this.svg.setAttribute("style", style);
    this.svg.setAttribute("fill", fill);
    this.svg.setAttribute("font-family", fontFamily);
  }

  extractReferences(figure){
    const svg = (figure.tagName === "FIGURE") ? (figure.childNodes[figure.childNodes.length - 1]) : ((figure.tagName === "DIV") ? figure.childNodes[1].childNodes[0] : figure);
    const style = svg.getAttribute("style");
    const fill = svg.getAttribute("fill");
    const fontFamily = svg.getAttribute("font-family");
    return [style, fill, fontFamily];
  }

  walkIntoSVG(svg){
    const g = this.create("g");
    const width = float(svg.getAttribute("width"));
    const height = float(svg.getAttribute("height"));
    this.extractSVG(svg, g, 0);
    this.svg.append(g);
    return [width, height];
  }

  create(element){
    return dom.window.document.createElementNS("http://www.w3.org/2000/svg", element);
  }

  getStyle(child){
    try { return dom.window.getComputedStyle(child)._values; } catch (error) { return {} }
  }

  makeH2(h2, width){
    const style = this.getStyle(h2);
    const text = this.create("text");
    const fontSize = this.convertUnit(style["font-size"]);
    text.setAttribute("dominant-baseline", "central");
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-size", `${fontSize}px`);
    text.setAttribute("x", width / 2);
    text.setAttribute("y", fontSize / 2);
    text.append(h2.childNodes[0].nodeValue);      
    return [text, fontSize];
  }

  makeText(child, width, height, x, y){
    const text = this.create("text");
    text.setAttribute("dominant-baseline", "central");
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-size", `${this.fontSize}px`);
    text.setAttribute("x", x !== 0 ? x + width : 0);
    text.setAttribute("y", y !== 0 ? y + height : 0);
    text.append(child.nodeValue);
    return text;
  }

  makeRect(g, width, height, x, y, style, counter){
      const rect = this.create("rect");
      const rectWidth = width + x + 10;
      const rectHeight = height + y;
      rect.setAttribute("width", rectWidth);
      rect.setAttribute("height", rectHeight);
      rect.setAttribute("x", -width / 2);
      rect.setAttribute("y", -height / 2);
      rect.setAttribute("fill", "none");
      rect.setAttribute("stroke", "none");

      const margin = this.convertUnit(style["margin-right"]) + this.convertUnit(style["margin-left"]);
      g.append(rect);
      g.setAttribute("transform", `translate(${(rectWidth + margin) * counter}, 0)`)
  }

  extractSVG(child, g, heightOffset){
    g.append(...Array.from(child.childNodes).filter(child => child.tagName !== "style"));
    const attributeNames = child.getAttributeNames().filter(name => !(avoidedAttributes.includes(name)));
    for (const name of attributeNames){
      g.setAttribute(name, child.getAttribute(name));
    }
    if (heightOffset !== 0){g.setAttribute("transform", `translate(0, ${heightOffset})`)}
  }

  walkInto(obj, support){
    let width = 0;
    let height = 0;
    let x = 0;
    let y = 0;
    let heightOffset = 0;
    let counter = -1;
    for (const child of obj.childNodes){
      if (child instanceof dom.window.Text) {
        support.append(this.makeText(child, width, height, x, y));
      } else {
        const style = this.getStyle(child);
        const g = this.create("g");
        switch(child.tagName){
          case "SPAN":
            counter += 1;
            [width, height, x, y] = this.walkInto(child, g);
            this.makeRect(g, width, height, x, y, style, counter);
            support.append(g);
            break;
          case "svg":
            width += float(child.getAttribute("width"));
            height += float(child.getAttribute("height"));
            x += this.convertUnit(style["margin-left"]) + this.convertUnit(style["margin-right"]);
            y += this.convertUnit(style["margin-top"]) + this.convertUnit(style["margin-bottom"]);
            this.extractSVG(child, g, heightOffset);
            support.append(g);
            break;
          case "DIV":
            const tempFontSize = this.convertUnit(style["font-size"])
            this.fontSize = (tempFontSize === 0) ? this.fontSize : tempFontSize;
            heightOffset = Math.max(
              Object.keys(style)
                    .filter(name => name.includes("height"))
                    .map(key => this.convertUnit(style[key]))
            );
            [width, height, x, y] = this.walkInto(child, g);
            if (Array.from(child.childNodes).length !== 1){
              g.setAttribute("transform", `translate(${width / 2}, ${heightOffset / 2})`); 
            }
            support.append(g);
            break;
          case "FIGURE":
            [width, height, x, y] = this.walkInto(child, support);
            break;
          default:
            break;
        }
      }
    }
    return [width, height + heightOffset, x, y];
  }

  convertUnit(string){
    if (string == undefined) {
      return 0;
    } else if (string.includes("px")) {
      return int(string.slice(0, -2));
    } else if (string.includes("em")) {
      return float(string) * this.fontSize;
    };
  }
}

function serialize(svg) {
  const fragment = dom.window.location.href + "#";
  const walker = dom.window.document.createTreeWalker(svg, 1);
  while (walker.nextNode()) {
    for (const attr of walker.currentNode.attributes) {
      if (attr.value.includes(fragment)) {
        attr.value = attr.value.replace(fragment, "#");
      }
    }
  }
  const serializer = new dom.window.XMLSerializer;
  const string = serializer.serializeToString(svg);
  return string;
};

function merge(svgs, grid) {
  if (svgs.length === 1){ return svgs[0]; }
  const svg = dom.window.document.createElementNS("http://www.w3.org/2000/svg", "svg");
  const ncols = grid;
  const nrows = Math.floor(svgs.length / grid) + Boolean(svgs.length % grid);
  const width = svgs.map(svg => (svg.getAttribute("width")))
                    .slice(0, ncols)
                    .reduce((partialSum, a) => partialSum + float(a), 0);
  const height = Array.from(Array(nrows).keys())
                      .map(i => svgs[i * ncols].getAttribute("height"))
                      .reduce((partialSum, a) => partialSum + float(a), 0);
  svg.setAttribute("width", width);
  svg.setAttribute("height", height);
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("style", svgs[0].getAttribute("style"));
  svg.setAttribute("fill", svgs[0].getAttribute("fill"));
  svg.setAttribute("font-family", svgs[0].getAttribute("font-family"));
  let dx = 0;
  let dy = 0;
  const localAvoidedAttributes = avoidedAttributes + ["fill", "style", "font-family"];
  for (const [index, child] of svgs.entries()){
    const g = dom.window.document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.append(...Array.from(child.childNodes));
    const attributeNames = child.getAttributeNames().filter(name => !(localAvoidedAttributes.includes(name)));
    for (const name of attributeNames){
      g.setAttribute(name, child.getAttribute(name));
    }
    if (dx !== 0 || dy !== 0){ g.setAttribute("transform", `translate(${dx}, ${dy})`); }
    const col  = (index + 1) % grid;
    dx = (col === 0) ? 0: dx + float(child.getAttribute("width", width));
    dy = (col === 0) ? dy + float(child.getAttribute("height", height)): dy;
    svg.append(g);
  }
  return svg;
}

let ws = new WebSocket("ws://localhost:5000");

ws.on("message", function message(received_data) {
  let data =  JSON.parse(received_data);

{% if plot %}{% if multiple %}{% for id, plot in code %}
  divs[{{ id }}].append({{ plot }});{% endfor %}{% else %}
  const plot = {{ code }};
  div.append(plot);
{% endif %}{% else %}
  {{ code }}
{% endif %}

{% if multiple %}
  const svgs = containers.map(figure => new Tracer(figure).svg);
  const output = merge(svgs, {{ grid }});
  ws.send(serialize(output));
{% else %}
  const figure = div.childNodes[0];
  const tracer = new Tracer(figure);
  ws.send(serialize(tracer.svg));
{% endif %}
  var end = performance.performance.now();
  console.log((end - start) * 1e-3);
});


