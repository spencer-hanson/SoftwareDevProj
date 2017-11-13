var width = 640,
    height = 480;


//links are source and target
var links =[
    {source: 'Baratheon', target: 'Lannister'},
    {source: 'Baratheon', target: 'Lannister'},
    {source: 'Lannister', target: 'Stark'},
    {source: 'Baratheon', target: 'Lannister'},
    {source: 'Baratheon', target: 'Lannister'},
    {source: 'Baratheon', target: 'Stark'},
    {source: 'Baratheon', target: 'Lannister'},
    {source: 'Stark', target: 'Lannister'},
];

var nodes = {};

//parse links to nodes

links.forEach(function(link) {
    links.source = nodes[link.source] || (nodes[link.source] = {name: link.source});

    link.target = nodes[link.target] || (nodes[link.target] = {name: link.target});


});


// add svg =
var svg = d3.select('body').append('svg')
    .attr('width', width)
    .attr("height", height);

var force = d3.layout.force()
    .size([width, height])
    .nodes(d3.values(nodes))
    .links(links)
    .on("tick", tick)
    .linkDistance(300)
    .start();


var link = svg.selectAll('.link')
    .data(links)
    .enter().append('line')
    .attr('class', 'link')

var node = svg.selectAll('.node')
    .data(force.nodes())
    .enter().append('circle')
    .attr('class, node')
    .attr('r', width * 0.03);

function tick(e) {
    node.attr('cx', function(d) {return d.x })
        .attr('cy', function(d) {return d.y})
        .call(force.drag);

    link.attr('x1', function(d) { return d.source.x; })
        .attr('y1', function(d) { return d.source.y; })
        .attr('x2', function(d) { return d.target.x; })
        .attr('y2', function(d) { return d.target.y; })
}


//up to 13:35 for https://www.youtube.com/watch?v=HP1tOlxVYz4