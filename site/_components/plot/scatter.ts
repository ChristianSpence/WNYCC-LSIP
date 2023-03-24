import d3 from "oi-lume-viz-beta/lib/external/d3.ts";
import { Colour } from "oi-lume-viz-beta/lib/colour/colour.ts";
import { Colour as ColourType } from "oi-lume-viz-beta/lib/colour/types.ts";

type Margin = {
  top: number;
  right: number;
  bottom: number;
  left: number;
};

type AxisDefinition = {
  title: string;
  padding: number;
}

interface ScatterPlotOptions {
  data: Record<string, number>[];
  x: string;
  y: string;
  axis?: {
    x?: Partial<AxisDefinition>;
    y?: Partial<AxisDefinition>;
  }
  width?: number;
  height?: number;
  margin?: Partial<Margin>;
  radius?: number;
  colour?: ColourType;
  nameMapper?: (d) => string;
}

class ScatterPlot {
  data: Record<string, number>[];
  x: string;
  y: string;
  height: number;
  width: number;
  margin: Margin;
  radius: number;
  colour: ColourType;
  nameMapper: (d) => string;
  xAxis: AxisDefinition;
  yAxis: AxisDefinition;

  constructor(options: ScatterPlotOptions) {
    this.data = structuredClone(options.data);
    this.x = options.x;
    this.y = options.y;
    this.width = options.width || 500;
    this.height = options.height || 300;
    this.margin = {
      left: 50,
      right: 10,
      top: 10,
      bottom: 50,
      ...options.margin,
    };
    this.radius = options.radius || 2;
    this.colour = Colour('#44aa22');
    this.nameMapper = options.nameMapper || ((d) => `${this.x}: ${d[this.x]}; ${this.y}: ${d[this.y]}`);
    this.xAxis = { title: this.x, padding: 30, ...options.axis?.x };
    this.yAxis = { title: this.y, padding: 40, ...options.axis?.y };
  }
  render() {
    const width = this.width + this.margin.left + this.margin.right;
    const height = this.height + this.margin.top + this.margin.bottom;
    const svg = d3.create("svg")
      .attr("viewBox", [-this.margin.left, -this.margin.top, width, height])
      .classed("oi-viz scatter-plot", true);

    const x = d3.scaleLinear()
      .domain([
        0,
        Math.max(...this.data.map((r) => r[this.x])),
      ])
      .range([0, this.width]);
    svg.append("g")
      .classed("axis", true)
      .attr("transform", "translate(0," + this.height + ")")
      .call(d3.axisBottom(x))
      .append('text')
        .attr("text-anchor", "middle")
        .attr("fill", "currentColor")
        .attr("x", this.width / 2)
        .attr("y", this.xAxis.padding)
        .text(this.xAxis.title );

    const y = d3.scaleLinear()
      .domain([
        Math.max(...this.data.map((r) => r[this.y])),
        0,
      ]).range([0, this.height]);
    svg.append("g")
      .classed("axis", true)
      .call(d3.axisLeft(y))
      .append('text')
        .attr("text-anchor", "middle")
        .attr("transform", `translate(-${this.yAxis.padding} ${this.height/2}) rotate(-90)`)
        .attr("fill", "currentColor")
        .attr("x", 0)
        .attr("y", 0)
        .text(this.yAxis.title );

    svg.append("g")
      .classed("series", true)
      .selectAll("dot")
      .data(this.data)
      .enter()
      .append("circle")
      .classed("point", true)
      .attr("cx", (d) => x(d[this.x]))
      .attr("cy", (d) => y(d[this.y]))
      .attr("r", this.radius)
      .attr('fill', this.colour.hex)
      .append('title')
        .text(this.nameMapper);

    return svg.node();
  }
}
export default function (options: {
  config: ScatterPlotOptions;
}) {
  const plot = new ScatterPlot(options.config);
  return plot.render();
}
