// Serialize svg object
function serialize(svg) {
  const fragment = window.location.href + "#";
  const walker = document.createTreeWalker(svg, NodeFilter.SHOW_ELEMENT);
  while (walker.nextNode()) {
    for (const attr of walker.currentNode.attributes) {
      if (attr.value.includes(fragment)) {
        attr.value = attr.value.replace(fragment, "#");
      }
    }
  }
  const serializer = new window.XMLSerializer;
  const string = serializer.serializeToString(svg);
  return string;
};
