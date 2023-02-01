import lume from "lume/mod.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import inline from "lume/plugins/inline.ts";
import minify_html from "lume/plugins/minify_html.ts";
import postcss from "lume/plugins/postcss.ts";
import oiCharts from "oi-lume-charts/mod.ts";
import csvLoader from "oi-lume-utils/loaders/csv-loader.ts";

const site = lume({
  src: "site",
});

site.use(base_path());
site.use(date());
site.use(inline());
site.use(minify_html());
site.use(postcss());
site.use(oiCharts({
  assetPath: "assets/oi",
  componentNamespace: "oi",
}));

site.loadData([".csv"], csvLoader);

const data = [
  "ks4/ks4.csv",
];

data.forEach((source) => {
  site.remoteFile(`_data/source/${source}`, `data/csv/${source}`);
});

site.remoteFile(
  "_includes/css/reset.css",
  "https://unpkg.com/modern-css-reset/dist/reset.css",
);

export default site;
