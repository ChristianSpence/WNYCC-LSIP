import lume from "lume/mod.ts";
import base_path from "lume/plugins/base_path.ts";
import date from "lume/plugins/date.ts";
import inline from "lume/plugins/inline.ts";
import metas from "lume/plugins/metas.ts";
import minify_html from "lume/plugins/minify_html.ts";
import postcss from "lume/plugins/postcss.ts";
import oiCharts from "oi-lume-charts/mod.ts";
import csvLoader from "oi-lume-utils/loaders/csv-loader.ts";

const search = { returnPageData: true };
const site = lume({
  src: "site",
  location: new URL('https://open-innovations.github.io/WNYCC-LSIP'),
}, { search });

site.use(base_path());
site.use(date());
site.use(inline());
site.use(metas());
site.use(postcss());
site.use(oiCharts({
  assetPath: "assets/oi",
  componentNamespace: "oi",
}));

site.use(minify_html());

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
