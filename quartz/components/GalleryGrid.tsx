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

  return (
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
          <a href={href} class="gallery-card internal">
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
  )
}

GalleryGrid.css = style
