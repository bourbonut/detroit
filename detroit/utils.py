from markupsafe import Markup

FETCH = Markup("var data;fetch(\"/data\").then(response => response.json()).then(d => {data = d;})")

SVG_SCRIPT = """<script>
    const xmlns = "http://www.w2.org/2000/xmlns/";
    const xlinkns = "http://www.w3.org/1999/xlink";
    const svgns = "http://www.w3.org/2000/svg";
    var mysvg;

    function waitForFigure(selector) {
      return new Promise(resolve => {
          if (document.getElementById(selector).childNodes[0]) {
              return resolve(document.getElementById(selector).childNodes[0]);
          }
    
          const observer = new MutationObserver(mutations => {
              if (document.getElementById(selector).childNodes[0]) {
                  observer.disconnect();
                  resolve(document.getElementById(selector).childNodes[0]);
              }
          });
    
          observer.observe(document.body, {
              childList: true,
              subtree: true
          });
      });
    }

    // Depending of the generated figure, sometimes the SVG content
    // is not at the root but on the first level of childs.
    function getSVG(figure) {
      if (figure.tagName === "svg"){
        return figure;
      } else {
        return Array.from(figure.childNodes).filter(e => e.tagName === "svg")[0];
      }
    }

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
      // svg.setAttributeNS(xmlns, "xmlns", svgns);
      // svg.setAttributeNS(xmlns, "xmlns:xlink", xlinkns);
      const serializer = new window.XMLSerializer;
      const string = serializer.serializeToString(svg);
      // return new Blob([string], {type: "image/svg+xml"});
      return string;
    };

    waitForFigure("myplot").then(figure => {mysvg = serialize(getSVG(figure))})
    // waitForFigure("myplot").then(figure => {
    //   fetch("/svg", {
    //     method: "POST",
    //     body: serialize(getSVG(figure))
    //   }) 
    // });
    </script>"""

def arrange(obj):
    try:
        import polars as pl
        if isinstance(obj, pl.DataFrame):
            return obj.to_dicts()
    except:
        pass
    try:
        import pandas as pd
        if isinstance(obj, pd.DataFrame):
            return obj.to_dict(orient="records")
    except:
        pass
    if isinstance(obj, list):
        if len(obj) == 1:
            obj = obj[0]
            if isinstance(obj, list):
                return [{"x": i, "y": item} for i, item in enumerate(obj)]
        elif len(obj) == 2:
            x, y = obj
            if isinstance(x, list) and isinstance(y, list):
                assert len(x) == len(y), "All inputs must have the same length."
                return [{"x": xi, "y": yi} for xi, yi in zip(x, y)]
            else:
                raise ValueError(f"Only list type supported.")
        elif len(obj) == 3:
            x, y, z = obj
            if all(map(lambda e: isinstance(e, list), (x, y, z))):
                assert len(x) == len(y) == len(z), "All inputs must have the same length."
                return [{"x": xi, "y": yi, "z": zi} for xi, yi, zi in zip(x, y, z)]
            else:
                raise ValueError(f"Only list type supported.")
    return obj
