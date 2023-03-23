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
    return d.data.unit_title;
  },
}