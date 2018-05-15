var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height");
    transform = d3.zoomIdentity;

var color = d3.scaleOrdinal(d3.schemeCategory20);

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));

var g = svg.append("g");
d3.json("twitter_graph.json", function(error, graph) {
  if (error) throw error;

  var link = g.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return Math.sqrt(d.value); });

  var node = g.append("g")
      .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
      .attr("r", function(d) {return (Math.sqrt(d.size) + 8);})
      .attr("fill", function(d) { return color(d.retweet); })
    
    .on("mouseover", function(d) {
        div.transition()
           .duration(200)
           .style("opacity", 0.9)
           .style("left", (d3.event.pageX - 5) + "px")
           .style("top", (d3.event.pageY - 80) + "px");

        div.html("<b>Author:</b> " + d.author +  "</br>" + "<b>Text:</b> " + d.text +  "</br> <b>Time Created</b>: " + d.time_created);
        // Current node gets bigger when moused-over
        d3.select(this).attr("r", function(d) {return 1.5*(Math.sqrt(d.size) + 8);});
     })
    .on("mouseout", function(d) {       
        div.transition()        
           .duration(500)      
           .style("opacity", 0)
           // Returning to the top left corner
           .style("left",  "0px")     
           .style("top", "0px");

        d3.select(this).attr("r", function(d) {return (Math.sqrt(d.size) + 8);});
    })
    .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));


  node.append("title")
      .text(function(d) { return d.text; });


  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);

  simulation.force("link")
      .links(graph.links);
    
var div = d3.select("body").append("div")	
      .attr("class", "tooltip")				
      .style("opacity", 0);

  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
    
  }
});





svg.call(d3.zoom()
    .scaleExtent([1 / 2, 8])
    .on("zoom", zoomed));
    
function zoomed() {
    g.attr("transform", d3.event.transform);
    }


function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

