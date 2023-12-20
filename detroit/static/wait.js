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
