import lume from "lume/mod.ts";
import jsonLoader from "lume/core/loaders/json.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import esbuild from "lume/plugins/esbuild.ts";
import inline from "lume/plugins/inline.ts";
import metas from "lume/plugins/metas.ts";
import minify_html from "lume/plugins/minify_html.ts";
import postcss from "lume/plugins/postcss.ts";
import oiCharts from "oi-lume-charts/mod.ts";
import csvLoader from "oi-lume-utils/loaders/csv-loader.ts";
import autoDependency from "oi-lume-utils/processors/auto-dependency.ts";
import { walkSync } from 'std/fs/mod.ts';

import * as treemap from "oi-lume-viz-beta/components/hierarchy/tree_map.ts";

const search = { returnPageData: true };
const site = lume({
  src: "site",
  location: new URL("https://open-innovations.github.io/WNYCC-LSIP"),
}, { search });

// Load TreeMap component
site.component("oi.viz.beta", {
  name: "tree_map",
  render: treemap.default,
});

site.use(date());
site.use(inline());
site.use(metas());
site.use(postcss());
site.use(oiCharts({
  assetPath: "/assets/oi",
  componentNamespace: "oi",
}));

site.use(esbuild({
  options: {
    format: "iife",
  }
}));

site.process([".html"], autoDependency);
site.use(base_path());
site.use(minify_html());

site.loadData([".csv"], csvLoader);
site.loadData([".hexjson"], jsonLoader);

site.remoteFile(
  "_includes/css/reset.css",
  "https://unpkg.com/modern-css-reset/dist/reset.css",
);

site.remoteFile("assets/oi/js/chart.js", "patch/chart.js");

site.filter("value_mapper", (data, config) => {
  const { key, mapper } = config;
  return data.map((v) => ({ ...v, [key]: mapper[v[key]] || v[key] }));
});

site.remoteFile(
  "assets/images/logo-white.svg",
  "https://www.wnychamber.co.uk/app/themes/wnychamber/dist/img/logo-white.svg",
);
site.remoteFile(
  "assets/images/lsip-web-logo.png",
  "https://www.wnychamber.co.uk/app/uploads/2023/01/LSIP-Web-Logo.png",
);

site.filter("localise", (num: number) => num.toLocaleString());
site.filter(
  "percentagize",
  (num: number, ref, points = 1) => (num * 100 / ref).toFixed(points) + "%",
);
site.filter("max", (arr: number[]) => (Math.max(...arr)));
site.filter("min", (arr: number[]) => (Math.min(...arr)));
site.filter(
  "row_sort",
  (data: Record<string, unknown>[], sortColumn: string, ascending = false) => {
    return data.sort((a, b) => {
      if (a[sortColumn] < b[sortColumn]) return ascending ? -1 : 1;
      if (a[sortColumn] > b[sortColumn]) return ascending ? 1 : -1;
      return 0;
    });
  },
);
site.filter("head", (arr: unknown[], count = 10) => arr.slice(0, count));


const dataDir = 'data/csv';
const dataPath = '/data/csv';
const dataFiles = Array.from(walkSync(dataDir, {
  includeDirs: false,
  exts: ["csv"],
})).map(({ path }) => path);
dataFiles.forEach(remote => {
  const local = remote.replace(dataDir, dataPath);
  site.remoteFile(local, './' + remote);
});
site.copy('/data');

export default site;
