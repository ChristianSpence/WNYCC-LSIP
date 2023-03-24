addEventListener("DOMContentLoaded", () => {
  const scatterPlots = document.querySelectorAll("svg.oi-viz.scatter-plot");
  const width = 200;
  scatterPlots.forEach((scatterPlot) => {
    const popup = document.createElement("aside");
    popup.classList.add("popup");
    popup.style.position = "fixed";
    popup.hidden = true;
    popup.style.opacity = "0";
    popup.style.width = width + "px";
    scatterPlot.after(popup);
    let fade: number | undefined = undefined;
    scatterPlot.addEventListener("mouseleave", function () {
      fade = setTimeout(() => {
        popup.style.opacity = "0";
        fade = setTimeout(() => {
          popup.hidden = true;
        }, 1000);
      }, 1000);
    });
    scatterPlot.querySelectorAll<SVGElement>(".series .point").forEach(
      (point) => {
        point.addEventListener("mouseover", function () {
          clearTimeout(fade);
          popup.innerHTML = this.querySelector("title")!.innerHTML;
          const { x, y } = this.getBoundingClientRect();
          popup.style.top = y + "px";
          popup.style.left = x - width / 2 + "px";
          popup.hidden = false;
          setTimeout(() => {
            popup.style.opacity = "1";
          }, 0);
        });
      },
    );
  });
});
