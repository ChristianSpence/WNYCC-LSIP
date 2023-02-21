export const layout = "layouts/metadata-report.njk";
export const tags = ["metadata"];

type SourceDefinition = {
  [origin: string]: {
    [source: string]: unknown;
  };
};

export default function* ({ source }: {
  source: SourceDefinition;
}) {
  for (const [origin, sources] of Object.entries(source)) {
    for (const [key, detail] of Object.entries(sources)) {
      const url = `/metadata/${origin}/${key}/`;
      yield {
        url,
        origin,
        title: key,
        fq_name: `${origin}/${key}`,
        metadata: detail,
      };
    }
  }
}
