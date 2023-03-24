import { Colour } from 'oi-lume-charts/lib/colour/colour.ts';
import { hslToHex } from 'oi-lume-charts/lib/colour/converters.ts';

export const soc4Demand = {
  grouper: [
    (d) => d.major_title,
    (d) => d.sub_major_title,
    (d) => d.minor_title,
  ],
  reducer: (d) => d,
  data: (d) => {
    if (Array.isArray(d.data)) d.data = { title: d.data[0], children: d.data[1] };
    if (d.height === 0 ) d.data.title = d.data.unit_title;
    if (d.data.title === undefined) d.data.title = 'SOC4 Code';
  },
  name: (d) => {
    if (!d.data.unit_title) return 'UNKNOWN';

    const { unit_title, minor_title, sub_major_title, major_title, count } = d.data;

    return `${
      [ major_title, sub_major_title, minor_title, unit_title ].join(' / ')
    }: ${ count.toLocaleString() } postings`;
  },
  colour: (d) => {
    const { major_title } = d.data;
    const colourTable = {
      'CARING, LEISURE AND OTHER SERVICE OCCUPATIONS': hslToHex(0, 70, 50),
      'All other postings': hslToHex(10, 70, 50),
      'PROFESSIONAL OCCUPATIONS': hslToHex(20, 70, 50),
      'ELEMENTARY OCCUPATIONS': hslToHex(30, 70, 50),
      'MANAGERS, DIRECTORS AND SENIOR OFFICIALS': hslToHex(40, 70, 50),
      'SKILLED TRADES OCCUPATIONS': hslToHex(50, 70, 50),
      'ADMINISTRATIVE AND SECRETARIAL OCCUPATIONS': hslToHex(60, 70, 50),
      'ASSOCIATE PROFESSIONAL AND TECHNICAL OCCUPATIONS': hslToHex(70, 70, 50),
      'SALES AND CUSTOMER SERVICE OCCUPATIONS': hslToHex(80, 70, 50),
      'PROCESS, PLANT AND MACHINE OPERATIVES': hslToHex(90, 70, 50),
    };
    if (!major_title) return "#aaaaaa";
    const colour = colourTable[major_title as string];
    return colour;
  }
}