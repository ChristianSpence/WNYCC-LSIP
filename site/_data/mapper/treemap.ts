import { hslToHex } from "oi-lume-charts/lib/colour/converters.ts";

export const soc4Demand = {
  grouper: [
    (d) => d.major_title,
    (d) => d.sub_major_title,
    (d) => d.minor_title,
  ],
  reducer: (d) => d,
  data: (d) => {
    if (Array.isArray(d.data)) {
      d.data = { title: d.data[0], children: d.data[1] };
    }
    if (d.height === 0) d.data.title = d.data.unit_title;
    if (d.data.title === undefined) d.data.title = "SOC4 Code";
  },
  name: (d) => {
    if (!d.data.unit_title) return "UNKNOWN";

    const { unit_title, minor_title, sub_major_title, major_title, count } =
      d.data;

    let title = [ major_title, sub_major_title, minor_title, unit_title ].join(' / ');
    if ( unit_title === 'All other postings' ) title = [ major_title, unit_title ].join(' / ');
    return `${ title }: ${ count.toLocaleString() } postings`;
  },
  colour: (d) => {
    const { major_title } = d.data;
    const colourTable = {
      "All other postings": hslToHex(0, 50, 50),
      "CARING, LEISURE AND OTHER SERVICE OCCUPATIONS": hslToHex(28, 80, 50),
      "PROFESSIONAL OCCUPATIONS": hslToHex(56, 80, 50),
      "ELEMENTARY OCCUPATIONS": hslToHex(84, 80, 50),
      "MANAGERS, DIRECTORS AND SENIOR OFFICIALS": hslToHex(112, 80, 50),
      "SKILLED TRADES OCCUPATIONS": hslToHex(140, 80, 50),
      "ADMINISTRATIVE AND SECRETARIAL OCCUPATIONS": hslToHex(168, 80, 50),
      "ASSOCIATE PROFESSIONAL AND TECHNICAL OCCUPATIONS": hslToHex(196, 80, 50),
      "SALES AND CUSTOMER SERVICE OCCUPATIONS": hslToHex(224, 80, 50),
      "PROCESS, PLANT AND MACHINE OPERATIVES": hslToHex(252, 80, 50),
    };
    if (!major_title) return "#aaaaaa";
    const colour = colourTable[major_title as string];
    return colour;
  },
};

export const supply_fe = {
  grouping: [
    (d) => 'Subject'
  ],
  reduce: (d) => d,
  colour: (d) => "#aaa",
  data: (d) => {
    if (d.height > 0) {
      d.data =  { title: d.data[0] || 'ROOT', children: d.data[1] };
    }
    if (d.height === 0) d.data.title = d.data.ssa_t1_desc;
  },
  name: (d) => {
    return `${d.data.ssa_t1_desc} had ${d.value} enrolments`;
  },
};
