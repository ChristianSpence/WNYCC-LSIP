import { hslToHex } from "oi-lume-charts/lib/colour/converters.ts";

export const soc4Demand = {
  tooltip: (d) => {
    const { unit_title, minor_title, sub_major_title, major_title, count } =
      d.data.original[0];

    if (!unit_title) return 'UNKNOWN';

    let title = [major_title, sub_major_title, minor_title, unit_title].join(
      ' / '
    );
    if (unit_title === 'All other postings') {
      title = [major_title, unit_title].join(' / ');
    }
    return `${title}: ${count.toLocaleString()} postings`;
  },
  colour: (d) => {
    const { major_title } = d.data.original[0];
    const colourTable = {
      'All other postings': hslToHex(0, 50, 50),
      'CARING, LEISURE AND OTHER SERVICE OCCUPATIONS': hslToHex(28, 80, 50),
      'PROFESSIONAL OCCUPATIONS': hslToHex(56, 80, 50),
      'ELEMENTARY OCCUPATIONS': hslToHex(84, 80, 50),
      'MANAGERS, DIRECTORS AND SENIOR OFFICIALS': hslToHex(112, 80, 50),
      'SKILLED TRADES OCCUPATIONS': hslToHex(140, 80, 50),
      'ADMINISTRATIVE AND SECRETARIAL OCCUPATIONS': hslToHex(168, 80, 50),
      'ASSOCIATE PROFESSIONAL AND TECHNICAL OCCUPATIONS': hslToHex(196, 80, 50),
      'SALES AND CUSTOMER SERVICE OCCUPATIONS': hslToHex(224, 80, 50),
      'PROCESS, PLANT AND MACHINE OPERATIVES': hslToHex(252, 80, 50),
    };
    if (!major_title) return '#aaaaaa';
    const colour = colourTable[major_title as string];
    return colour;
  },
};

export const supply_fe = {
  colour: (d) => {
    const { ssa_t1_desc } = d.data.original[0];
    const colourTable = {
      'Agriculture, Horticulture and Animal Care': hslToHex(16, 50, 50),
      'Arts, Media and Publishing': hslToHex(32, 50, 50),
      'Business, Administration and Law': hslToHex(48, 50, 50),
      'Construction, Planning and the Built Environment': hslToHex(64, 50, 50),
      'Education and Training': hslToHex(80, 50, 50),
      'Engineering and Manufacturing Technologies': hslToHex(96, 50, 50),
      'Health, Public Services and Care': hslToHex(112, 50, 50),
      'History, Philosophy and Theology': hslToHex(128, 50, 50),
      'Information and Communication Technology': hslToHex(144, 50, 50),
      'Languages, Literature and Culture': hslToHex(160, 50, 50),
      'Leisure, Travel and Tourism': hslToHex(176, 50, 50),
      'Not Applicable/ Not Known': hslToHex(192, 50, 50),
      'Preparation for Life and Work': hslToHex(208, 50, 50),
      'Retail and Commercial Enterprise': hslToHex(224, 50, 50),
      'Science and Mathematics': hslToHex(240, 50, 50),
      'Social Sciences': hslToHex(256, 50, 50),
    };
    if (!ssa_t1_desc) return '#aaaaaa';
    const colour = colourTable[ssa_t1_desc as string];
    return colour;
  },
};
