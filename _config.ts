import lume from "lume/mod.ts";
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
  location: new URL('https://open-innovations.github.io/WNYCC-LSIP'),
}, { search });

site.use(date());
site.use(inline());
site.use(metas());
site.use(postcss());
site.use(oiCharts({
  assetPath: "/assets/oi",
  componentNamespace: "oi",
}));

site.process(['.html'], autoDependency);
site.use(base_path());
site.use(minify_html());

site.loadData([".csv"], csvLoader);

site.remoteFile(
  "_includes/css/reset.css",
  "https://unpkg.com/modern-css-reset/dist/reset.css",
);

site.filter('value_mapper', (data, config) => {
  const { key, mapper } = config;
  return data.map(v => ({ ...v, [key]: mapper[v[key]] || v[key] }));
})

export default site;
