export const postingsDemandDuration = (d) => `
Skill "${d.skill}" had ${d.count} postings with an average posting duration of ${d.duration.toFixed(1)} days
in ${d.geography_name}`;