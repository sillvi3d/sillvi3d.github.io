import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/imageLightbox.scss"

interface ImageLightboxOptions {
  /** Only activate on pages whose slug starts with one of these prefixes */
  folderPrefixes?: string[]
}

const defaultOptions: ImageLightboxOptions = {
  folderPrefixes: ["1_Works"],
}

export default ((userOpts?: Partial<ImageLightboxOptions>) => {
  const opts = { ...defaultOptions, ...userOpts }

  // Serialize folder prefixes into the DOM so afterDOMLoaded can read them
  const ImageLightbox: QuartzComponent = (_props: QuartzComponentProps) => {
    return (
      <div
        id="image-lightbox-config"
        data-prefixes={JSON.stringify(opts.folderPrefixes)}
        style="display:none"
      />
    )
  }

  ImageLightbox.css = style

  ImageLightbox.afterDOMLoaded = `
    document.addEventListener("nav", () => {
      // Read config
      const configEl = document.getElementById("image-lightbox-config")
      if (!configEl) return
      const prefixes = JSON.parse(configEl.getAttribute("data-prefixes") || "[]")

      // Check if current page matches
      const slug = document.body.getAttribute("data-slug") || ""
      const isTarget = prefixes.some((p) => slug.startsWith(p + "/"))
      if (!isTarget) return

      // Skip index pages
      if (slug.endsWith("/index") || slug.endsWith("/")) return

      // Collect all images in the article
      const article = document.querySelector("article")
      if (!article) return
      const images = Array.from(article.querySelectorAll("img"))
      if (images.length === 0) return

      // Remove any existing lightbox (SPA nav)
      const existing = document.getElementById("img-lightbox")
      if (existing) existing.remove()

      // Create lightbox DOM
      const overlay = document.createElement("div")
      overlay.id = "img-lightbox"
      overlay.className = "img-lightbox"
      overlay.innerHTML = \`
        <div class="lb-backdrop"></div>
        <button class="lb-close" aria-label="Close">&times;</button>
        <button class="lb-prev" aria-label="Previous">&#8249;</button>
        <button class="lb-next" aria-label="Next">&#8250;</button>
        <div class="lb-img-wrap">
          <img class="lb-img" src="" alt="" />
        </div>
        <div class="lb-counter"></div>
      \`
      document.body.appendChild(overlay)

      const lbImg = overlay.querySelector(".lb-img")
      const lbCounter = overlay.querySelector(".lb-counter")
      const lbPrev = overlay.querySelector(".lb-prev")
      const lbNext = overlay.querySelector(".lb-next")
      const lbClose = overlay.querySelector(".lb-close")
      const lbBackdrop = overlay.querySelector(".lb-backdrop")

      let currentIdx = 0

      function show(idx) {
        currentIdx = idx
        lbImg.src = images[idx].src
        lbImg.alt = images[idx].alt || ""
        lbCounter.textContent = (idx + 1) + " / " + images.length
        lbPrev.style.display = images.length > 1 ? "" : "none"
        lbNext.style.display = images.length > 1 ? "" : "none"
        overlay.classList.add("lb-open")
        document.body.style.overflow = "hidden"
      }

      function hide() {
        overlay.classList.remove("lb-open")
        document.body.style.overflow = ""
      }

      function prev() {
        show((currentIdx - 1 + images.length) % images.length)
      }

      function next() {
        show((currentIdx + 1) % images.length)
      }

      // Bind image clicks
      images.forEach((img, i) => {
        img.style.cursor = "zoom-in"
        img.addEventListener("click", (e) => {
          e.preventDefault()
          e.stopPropagation()
          show(i)
        })
      })

      // Controls
      lbClose.addEventListener("click", hide)
      lbBackdrop.addEventListener("click", hide)
      lbPrev.addEventListener("click", prev)
      lbNext.addEventListener("click", next)

      // Keyboard
      function onKey(e) {
        if (!overlay.classList.contains("lb-open")) return
        if (e.key === "Escape") hide()
        else if (e.key === "ArrowLeft") prev()
        else if (e.key === "ArrowRight") next()
      }
      document.addEventListener("keydown", onKey)

      // Touch swipe
      let touchStartX = 0
      overlay.addEventListener("touchstart", (e) => {
        touchStartX = e.changedTouches[0].clientX
      }, { passive: true })
      overlay.addEventListener("touchend", (e) => {
        const dx = e.changedTouches[0].clientX - touchStartX
        if (Math.abs(dx) > 50) {
          dx > 0 ? prev() : next()
        }
      }, { passive: true })
    })
  `

  return ImageLightbox
}) satisfies QuartzComponentConstructor
