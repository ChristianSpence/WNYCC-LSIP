addEventListener("DOMContentLoaded", () => {
  const treemaps = document.querySelectorAll("svg.treemap");
  const width = 200;
  treemaps.forEach((treemap) => {
    const popup: HTMLElement = document.createElement("aside");
    popup.classList.add("popup", "treemap");
    popup.style.position = "fixed";
    popup.style.opacity = '0';
    popup.style.width = width + 'px';
    popup.style.pointerEvents = 'none'
    // popup.hidden = true;
    treemap.after(popup);
    let fader: number | undefined = undefined;
    treemap.addEventListener("mouseleave", function () {
      //   popup.hidden = true;
      fader = setTimeout(
        () => {
          popup.style.opacity = '0';
          fader = setTimeout(() => {
            popup.hidden = true;
          }, 1000)
        }, 1000);
    });

    const nodes = treemap.querySelectorAll<SVGElement>(".series");
    nodes.forEach((node) => {
      node.addEventListener("mouseover", function () {
        popup.innerHTML = this.querySelector("rect title")?.innerHTML || '';
        popup.hidden = false;
        popup.style.opacity = '1';
        clearTimeout(fader);
      });
      node.addEventListener("mousemove", function (event) {
        clearTimeout(fader);
        popup.style.left = event.clientX - width / 2 + "px";
        popup.style.top = event.clientY + "px";
      });
    });
  });
});
