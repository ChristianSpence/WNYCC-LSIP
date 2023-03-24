addEventListener("DOMContentLoaded", () => {
  const plotSelector = "svg.oi-viz.scatter-plot";
  const width = 200;
  const targetSelector = ".series .point";
  const titleSelector = "title";

  const plots = document.querySelectorAll<SVGElement>(plotSelector);

  plots.forEach((plot) => {
    // Create the popup
    const popup: HTMLElement = document.createElement("aside");
    popup.classList.add("popup");
    popup.style.position = "fixed";
    popup.hidden = true;
    popup.style.opacity = "0";
    popup.style.width = width + "px";
    popup.style.pointerEvents = "none";

    // Add just after the SVG
    plot.after(popup);

    let fader: number | undefined = undefined;
    plot.addEventListener("mouseleave", function () {
      fader = setTimeout(
        () => {
          popup.style.opacity = "0";
          fader = setTimeout(() => {
            popup.hidden = true;
          }, 1000);
        },
        1000,
      );
    });

    plot.querySelectorAll<SVGElement>(targetSelector).forEach(
      (target) => {
        target.addEventListener("mouseover", function () {
          clearTimeout(fader);
          popup.innerHTML = this.querySelector(titleSelector)?.innerHTML || "";
          const { x, y } = this.getBoundingClientRect();
          popup.style.left = x - width / 2 + "px";
          popup.style.top = y + "px";
          popup.hidden = false;
          setTimeout(() => {
            popup.style.opacity = "1";
          }, 0);
        });
      },
    );
  });
});
