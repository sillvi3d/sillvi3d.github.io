import { resolveRelative, pathToRoot, FullSlug, joinSegments } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { Date, getDate } from "./Date"
import { QuartzComponent, QuartzComponentProps } from "./types"
import { GlobalConfiguration } from "../cfg"
import { byDateAndAlphabeticalFolderFirst, SortFn } from "./PageList"

import style from "./styles/gallery.scss"

type GalleryProps = {
  limit?: number
  sort?: SortFn
} & QuartzComponentProps

export const GalleryGrid: QuartzComponent = ({
  cfg,
  fileData,
  allFiles,
  limit,
  sort,
}: GalleryProps) => {
  const sorter = sort ?? byDateAndAlphabeticalFolderFirst(cfg)
  let list = allFiles.sort(sorter)
  if (limit) {
    list = list.slice(0, limit)
  }

  // Collect all unique tags for the filter bar
  const allTags = new Set<string>()
  list.forEach((page) => {
    const tags = page.frontmatter?.tags ?? []
    tags.forEach((t: string) => allTags.add(t))
  })
  const sortedTags = [...allTags].sort()

  return (
    <div class="gallery-container">
      {/* Tag filter bar */}
      {sortedTags.length > 0 && (
        <div class="gallery-filter-bar">
          <button class="gallery-filter-btn gf-active" data-tag="all">All</button>
          {sortedTags.map((tag) => (
            <button class="gallery-filter-btn" data-tag={tag}>{tag}</button>
          ))}
        </div>
      )}

      <div class="gallery-grid">
        {list.map((page) => {
          const title = page.frontmatter?.title
          const thumbnail = (page.frontmatter as any)?.thumbnail
          const tags = page.frontmatter?.tags ?? []
          const description = (page.frontmatter as any)?.description ?? ""
          const href = resolveRelative(fileData.slug!, page.slug!)
          const date = getDate(cfg, page)
          const dateStr = date
            ? date.toLocaleDateString("ko-KR", { year: "numeric", month: "short", day: "numeric" })
            : ""

          return (
            <a
              href={href}
              class="gallery-card internal"
              data-tags={tags.join(",")}
            >
              <div class="gallery-card-img">
                {thumbnail ? (
                  <img
                    src={joinSegments(pathToRoot(fileData.slug!), thumbnail)}
                    alt={title ?? ""}
                    loading="lazy"
                  />
                ) : (
                  <div class="gallery-card-placeholder">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="48"
                      height="48"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1.5"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                    >
                      <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                      <circle cx="8.5" cy="8.5" r="1.5" />
                      <polyline points="21 15 16 10 5 21" />
                    </svg>
                  </div>
                )}
                {/* Hover overlay */}
                <div class="gallery-card-overlay">
                  {dateStr && <span class="gallery-overlay-date">{dateStr}</span>}
                  {description && <p class="gallery-overlay-desc">{description}</p>}
                </div>
              </div>
              <div class="gallery-card-meta">
                <h3>{title}</h3>
                {tags.length > 0 && (
                  <ul class="tags">
                    {tags.map((tag) => (
                      <li>
                        <span class="tag-link">{tag}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </a>
          )
        })}
      </div>
    </div>
  )
}

GalleryGrid.css = style

GalleryGrid.afterDOMLoaded = `
  document.addEventListener("nav", () => {
    document.querySelectorAll(".gallery-filter-bar").forEach((bar) => {
      const container = bar.closest(".gallery-container")
      if (!container) return
      const grid = container.querySelector(".gallery-grid")
      if (!grid) return

      const buttons = bar.querySelectorAll(".gallery-filter-btn")
      let activeTag = "all"

      function applyFilter() {
        // Update button states
        buttons.forEach((btn) => {
          if (btn.getAttribute("data-tag") === activeTag) {
            btn.classList.add("gf-active")
          } else {
            btn.classList.remove("gf-active")
          }
        })

        // Show/hide cards
        grid.querySelectorAll(".gallery-card").forEach((card) => {
          if (activeTag === "all") {
            card.style.display = ""
          } else {
            const cardTags = (card.getAttribute("data-tags") || "").split(",")
            card.style.display = cardTags.includes(activeTag) ? "" : "none"
          }
        })
      }

      buttons.forEach((btn) => {
        btn.addEventListener("click", (e) => {
          e.preventDefault()
          activeTag = btn.getAttribute("data-tag") || "all"
          applyFilter()
        })
      })
    })
  })
`
