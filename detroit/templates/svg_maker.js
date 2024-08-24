{{ import_package }}
import { JSDOM } from "jsdom";
import WebSocket from "ws";
import performance from "perf_hooks";
const dom = new JSDOM();

var start = performance.performance.now();
let heading = dom.window.document.createElement("div");
dom.window.document.body.appendChild(heading);
heading.id = "myplot";

const avoidedAttributes = ["viewBox", "class", "width", "height"];

// Convenient function to convert a string into integer
function int(string){
  return parseInt(string, 10);
}

function float(string){
  return parseFloat(string);
}

class Tracer {
  constructor(figure, grid = 1) {
    const svg = (figure.tagName == "FIGURE") ? figure.childNodes[figure.childNodes.length - 1] : figure
    this.fontSize = 10;
    this.grid = grid;
    this.svg = this.create("svg");
    const [width, height] = this.walkInto(figure, this.svg).slice(0, 2);
    this.svg.setAttribute("width", width);
    this.svg.setAttribute("height", height);
    this.svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
    this.svg.setAttribute("style", svg.getAttribute("style"));
    this.svg.setAttribute("fill", svg.getAttribute("fill"));
    this.svg.setAttribute("font-family", svg.getAttribute("font-family"));
  }

  create(element){
    return dom.window.document.createElementNS("http://www.w3.org/2000/svg", element);
  }

  getStyle(child){
    try { return dom.window.getComputedStyle(child)._values; } catch (error) { return {} }
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
            this.fontSize = this.convertUnit(style["font-size"])
            heightOffset = Math.max(
              Object.keys(style)
                    .filter(name => name.includes("height"))
                    .map(key => this.convertUnit(style[key]))
            );
            [width, height, x, y] = this.walkInto(child, g);
            g.setAttribute("transform", `translate(${width / 2}, ${heightOffset / 2})`);
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

let ws = new WebSocket("ws://localhost:5000");

ws.on("message", function message(received_data) {
  let data =  JSON.parse(received_data);

{% if plot %}
  const plot = {{ code }};
  heading.append(plot);
{% else %}
  {{ code }}
{% endif %}

  const figure = heading.childNodes[0];
  const tracer = new Tracer(figure);
  var end = performance.performance.now();
  ws.send(serialize(tracer.svg));
  console.log((end - start) * 1e-3);
});


