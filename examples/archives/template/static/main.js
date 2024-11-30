var cache = [];

document.querySelector("#longitude-number").oninput = function(){
  // Update values
  document.querySelector("#longitude-range").value = document.querySelector("#longitude-number").value;
  // Build the earth globe
  build(cache[0], cache[1]);
}

document.querySelector("#longitude-range").oninput = function(){
  // Update values
  document.querySelector("#longitude-number").value = document.querySelector("#longitude-range").value;
  // Build the earth globe
  build(cache[0], cache[1]);
}

// Fetch data one and save them to the cache variable
async function fetchData(){
  const earthquakes = await d3.json("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_week.geojson").then(d => d.features.map(f => {
    const c = d3.geoCentroid(f);
    return {magnitude: f.properties.mag, longitude: c[0], latitude: c[1]};
  }))

  const response = await fetch("https://static.observableusercontent.com/files/7c6167b65013c12f3978b4d8e85dd28a27e3b5eb580d1e76696ce5b0d399c196de2b02c45e734462931e1af823698e36bb072722253d5e03e7fb61222755bc0c");
  const world = await response.json();
  const land = topojson.feature(world, world.objects.land);
  cache = [earthquakes, land];
  build(earthquakes, land);
}

// Build the earth globe
async function build(earthquakes, land) {
  const div = document.querySelector("#earth-globe"); // get div
  const longitude = document.querySelector("#longitude-range").value; // get longitude value
  const plot = Plot.plot({'projection': {'type': 'orthographic', 'rotate': [-longitude, -30]}, 'r': {'transform': (d) => Math.pow(10, d)}, 'style': 'overflow: visible;', 'marks': [Plot.geo(land, {'fill': 'currentColor', 'fillOpacity': 0.2}), Plot.sphere(), Plot.dot(earthquakes, {'x': 'longitude', 'y': 'latitude', 'r': 'magnitude', 'stroke': 'red', 'fill': 'red', 'fillOpacity': 0.2})]}); // code from python
  if (div.innerHTML) {
    div.innerHTML = "";
    div.append(plot);
  } else {
    div.append(plot);
  } 
}

fetchData();