import lume from "lume/mod.ts";
import jsonLoader from "lume/core/loaders/json.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import inline from "lume/plugins/inline.ts";
import metas from "lume/plugins/metas.ts";
import minify_html from "lume/plugins/minify_html.ts";
import postcss from "lume/plugins/postcss.ts";
import oiCharts from "oi-lume-charts/mod.ts";
import csvLoader from "oi-lume-utils/loaders/csv-loader.ts";
import autoDependency from "oi-lume-utils/processors/auto-dependency.ts";

const search = { returnPageData: true };
const site = lume({
  src: "site",
  location: new URL("https://open-innovations.github.io/WNYCC-LSIP"),
}, { search });

site.use(date());
site.use(inline());
site.use(metas());
site.use(postcss());
site.use(oiCharts({
  assetPath: "/assets/oi",
  componentNamespace: "oi",
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

export default site;
