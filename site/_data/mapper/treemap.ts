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

export const industry_sector = {
  colour: (d) => {
    const { industry_name } = d.data.original[0];
    const colourTable = {
      "A : Agriculture, forestry and fishing": hslToHex(11, 50, 50),
      "B : Mining and quarrying": hslToHex(22, 50, 50),
      "C : Manufacturing": hslToHex(33, 50, 50),
      "D : Electricity, gas, steam and air conditioning supply": hslToHex(44, 50, 50),
      "E : Water supply; sewerage, waste management and remediation activities": hslToHex(55, 50, 50),
      'F : Construction': hslToHex(66, 50, 50),
      'G : Wholesale and retail trade; repair of motor vehicles and motorcycles': hslToHex(77, 50, 50),
      "H : Transportation and storage": hslToHex(88, 50, 50),
      "I : Accommodation and food service activities": hslToHex(99, 50, 50),
      "J : Information and communication": hslToHex(110, 50, 50),
      "K : Financial and insurance activities": hslToHex(121, 50, 50),
      "L : Real estate activities": hslToHex(132, 50, 50),
      "M : Professional scientific and technical activities": hslToHex(143, 50, 50),
      "N : Administrative and support service activities": hslToHex(154, 50, 50),
      "O : Public administration and defence; compulsory social security": hslToHex(165, 50, 50),
      "P : Education": hslToHex(176, 50, 50),
      "Q : Human health and social work activities": hslToHex(187, 50, 50),
      "R : Arts entertainment and recreation": hslToHex(198, 50, 50),
      "S : Other service activities": hslToHex(209, 50, 50),
      "T : Activities of households as employers;undifferentiated goods-and services-producing activities of households for own use": hslToHex(220, 50, 50),
      "U : Activities of extraterritorial organisations and bodies": hslToHex(256, 50, 50),
    };
    if (!industry_name) return '#aaaaaa';
    const colour = colourTable[industry_name as string];
    return colour;
  },
};
