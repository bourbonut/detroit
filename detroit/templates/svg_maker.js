import * as d3 from "d3";
import * as jsdom from "jsdom";
import WebSocket from "ws";
const { JSDOM } = jsdom;
const dom = new JSDOM();

let heading = dom.window.document.createElement("div");
dom.window.document.body.appendChild(heading);
heading.id = "myplot";

let ws = new WebSocket("ws://localhost:5000");

ws.on("message", function message(received_data) {
  let data =  JSON.parse(received_data);

  {{ code }}

  console.log(heading.innerHTML);
});

