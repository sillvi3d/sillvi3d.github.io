import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { resolveRelative, pathToRoot, joinSegments, FullSlug } from "../util/path"
import { QuartzPluginData } from "../plugins/vfile"
import { getDate } from "./Date"

import style from "./styles/recentWorks.scss"

interface RecentWorksOptions {
  /** Sections to display, each with a title and folder prefix */
  sections: { title: string; folder: string }[]
  /** Number of items per section */
  limit: number
}

const defaultOptions: RecentWorksOptions = {
  sections: [
    { title: "3D", folder: "1_Works/3D" },
    { title: "AI", folder: "1_Works/AI" },
  ],
  limit: 3,
}

export default ((userOpts?: Partial<RecentWorksOptions>) => {
  const opts = { ...defaultOptions, ...userOpts }

  const RecentWorks: QuartzComponent = (props: QuartzComponentProps) => {
    const { cfg, fileData, allFiles } = props

    // Filter out index files and drafts, only include actual content pages
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
        .slice(0, opts.limit)

      return { ...section, files }
    })

    // Don't render if there are no works at all
    const totalFiles = sections.reduce((sum, s) => sum + s.files.length, 0)
    if (totalFiles === 0) return null

    return (
      <div class="recent-works">
        <h2 class="recent-works-title">Recent Works</h2>
        {sections.map((section) => (
          <div class="recent-works-section">
            <h3 class="recent-works-section-title">
              <a
                href={resolveRelative(fileData.slug!, (section.folder + "/") as FullSlug)}
                class="internal"
              >
                {section.title}
              </a>
            </h3>
            {section.files.length > 0 ? (
              <div class="recent-works-grid">
                {section.files.map((page) => {
                  const title = page.frontmatter?.title
                  const thumbnail = (page.frontmatter as any)?.thumbnail
                  const href = resolveRelative(fileData.slug!, page.slug!)

                  return (
                    <a href={href} class="recent-works-card internal">
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
            ) : (
              <p class="recent-works-empty">아직 작업물이 없습니다.</p>
            )}
          </div>
        ))}
      </div>
    )
  }

  RecentWorks.css = style
  return RecentWorks
}) satisfies QuartzComponentConstructor
