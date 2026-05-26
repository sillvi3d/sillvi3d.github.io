import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative, pathToRoot, joinSegments, FullSlug } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { getDate } from "./Date"

import style from "./styles/recentWorks.scss"

interface RecentWorksOptions {
  /** Sections to display, each with a title and folder prefix */
  sections: { title: string; folder: string }[]
  /** Number of items per page */
  perPage: number
}

const defaultOptions: RecentWorksOptions = {
  sections: [
    { title: "3D", folder: "1_Works/3D" },
    { title: "AI", folder: "1_Works/AI" },
  ],
  perPage: 6,
}

export default ((userOpts?: Partial<RecentWorksOptions>) => {
  const opts = { ...defaultOptions, ...userOpts }

  const RecentWorks: QuartzComponent = (props: QuartzComponentProps) => {
    const { cfg, fileData, allFiles } = props

    const contentFiles = allFiles.filter(
      (f) => f.slug && !f.slug.endsWith("/index") && !f.frontmatter?.draft,
    )

    const sections = opts.sections.map((section) => {
      const files = contentFiles
        .filter((f) => f.slug?.startsWith(section.folder + "/"))
        .sort((a, b) => {
          const dateA = getDate(cfg, a)
          const dateB = getDate(cfg, b)
          if (dateA && dateB) return dateB.getTime() - dateA.getTime()
          if (dateA) return -1
          if (dateB) return 1
          return 0
        })

      return { ...section, files }
    })

    const totalFiles = sections.reduce((sum, s) => sum + s.files.length, 0)
    if (totalFiles === 0) return null

    return (
      <div class="recent-works">
        <h2 class="recent-works-title">Recent Works</h2>
        {sections.map((section, sIdx) => {
          const totalPages = Math.max(1, Math.ceil(section.files.length / opts.perPage))

          return (
            <div class="recent-works-section" data-section-id={`rw-section-${sIdx}`}>
              <h3 class="recent-works-section-title">
                <a
                  href={resolveRelative(fileData.slug!, (section.folder + "/") as FullSlug)}
                  class="internal"
                >
                  {section.title}
                </a>
              </h3>
              {section.files.length > 0 ? (
                <>
                  <div class="recent-works-grid" data-per-page={opts.perPage}>
                    {section.files.map((page, i) => {
                      const title = page.frontmatter?.title
                      const thumbnail = (page.frontmatter as any)?.thumbnail
                      const href = resolveRelative(fileData.slug!, page.slug!)
                      const pageNum = Math.floor(i / opts.perPage)

                      return (
                        <a
                          href={href}
                          class={`recent-works-card internal ${pageNum === 0 ? "" : "rw-hidden"}`}
                          data-rw-page={pageNum}
                        >
                          <div class="recent-works-card-img">
                            {thumbnail ? (
                              <img
                                src={joinSegments(pathToRoot(fileData.slug!), thumbnail)}
                                alt={title ?? ""}
                                loading="lazy"
                              />
                            ) : (
                              <div class="recent-works-placeholder">
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width="36"
                                  height="36"
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
                          </div>
                          <div class="recent-works-card-meta">
                            <span>{title}</span>
                          </div>
                        </a>
                      )
                    })}
                  </div>
                  {totalPages > 1 && (
                    <div class="rw-pagination" data-total-pages={totalPages} data-current-page="0">
                      <button class="rw-page-btn rw-first" title="First">&laquo;</button>
                      <button class="rw-page-btn rw-prev" title="Previous">&lsaquo;</button>
                      <span class="rw-page-numbers"></span>
                      <button class="rw-page-btn rw-next" title="Next">&rsaquo;</button>
                      <button class="rw-page-btn rw-last" title="Last">&raquo;</button>
                    </div>
                  )}
                </>
              ) : (
                <p class="recent-works-empty">아직 작업물이 없습니다.</p>
              )}
            </div>
          )
        })}
      </div>
    )
  }

  RecentWorks.css = style

  RecentWorks.afterDOMLoaded = `
    document.addEventListener("nav", () => {
      document.querySelectorAll(".rw-pagination").forEach((pag) => {
        const section = pag.closest(".recent-works-section")
        if (!section) return
        const grid = section.querySelector(".recent-works-grid")
        if (!grid) return

        const totalPages = parseInt(pag.getAttribute("data-total-pages") || "1")
        let currentPage = 0

        function render() {
          // Show/hide cards
          grid.querySelectorAll(".recent-works-card").forEach((card) => {
            const p = parseInt(card.getAttribute("data-rw-page") || "0")
            if (p === currentPage) {
              card.classList.remove("rw-hidden")
            } else {
              card.classList.add("rw-hidden")
            }
          })

          // Update page numbers
          const numbersEl = pag.querySelector(".rw-page-numbers")
          if (numbersEl) {
            numbersEl.innerHTML = ""
            for (let i = 0; i < totalPages; i++) {
              const btn = document.createElement("button")
              btn.className = "rw-page-num" + (i === currentPage ? " rw-active" : "")
              btn.textContent = String(i + 1)
              btn.addEventListener("click", () => { currentPage = i; render() })
              numbersEl.appendChild(btn)
            }
          }

          // Update button states
          pag.querySelector(".rw-first").disabled = currentPage === 0
          pag.querySelector(".rw-prev").disabled = currentPage === 0
          pag.querySelector(".rw-next").disabled = currentPage === totalPages - 1
          pag.querySelector(".rw-last").disabled = currentPage === totalPages - 1

          pag.setAttribute("data-current-page", String(currentPage))
        }

        pag.querySelector(".rw-first").addEventListener("click", () => { currentPage = 0; render() })
        pag.querySelector(".rw-prev").addEventListener("click", () => { currentPage = Math.max(0, currentPage - 1); render() })
        pag.querySelector(".rw-next").addEventListener("click", () => { currentPage = Math.min(totalPages - 1, currentPage + 1); render() })
        pag.querySelector(".rw-last").addEventListener("click", () => { currentPage = totalPages - 1; render() })

        render()
      })
    })
  `

  return RecentWorks
}) satisfies QuartzComponentConstructor
