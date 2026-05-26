import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/softwareUsed.scss"

/**
 * Software mapping: frontmatter key → display info
 * - name: 블로그에 표시될 이름
 * - short: 로고 대신 보여줄 약자 (1~3자)
 * - color: 브랜드 컬러 (약자 배경색)
 *
 * 새 소프트웨어 추가는 여기에 한 줄만 추가하면 됩니다.
 */
const SOFTWARE_MAP: Record<string, { name: string; short: string; color: string }> = {
  // 3D — Main
  "unreal-engine":      { name: "Unreal Engine",      short: "UE",  color: "#313131" },
  "speedtree":          { name: "SpeedTree",           short: "ST",  color: "#6B8E23" },
  "megascans":          { name: "Megascans",           short: "MS",  color: "#1a1a2e" },
  "comfyui":            { name: "ComfyUI",             short: "C",   color: "#7B68EE" },
  // 3D — Sub
  "blender":            { name: "Blender",             short: "B",   color: "#EA7600" },
  "substance-painter":  { name: "Substance Painter",   short: "Pt",  color: "#FF6B4A" },
  // 추가 예비 슬롯 (필요 시 주석 해제)
  // "maya":            { name: "Maya",                short: "M",   color: "#00827F" },
  // "zbrush":          { name: "ZBrush",              short: "ZB",  color: "#EC6E2A" },
  // "substance-designer": { name: "Substance Designer", short: "Sd", color: "#FF6B4A" },
  // "marmoset":        { name: "Marmoset Toolbag",    short: "MT",  color: "#3D3D3D" },
  // "houdini":         { name: "Houdini",             short: "H",   color: "#FF4713" },
  // "midjourney":      { name: "Midjourney",          short: "MJ",  color: "#5865F2" },
  // "stable-diffusion":{ name: "Stable Diffusion",    short: "SD",  color: "#A855F7" },
  // "meshy":           { name: "Meshy",               short: "Me",  color: "#6366F1" },
  // "tripo":           { name: "Tripo",               short: "Tr",  color: "#0EA5E9" },
}

interface SoftwareUsedOptions {
  /** Only show on pages whose slug starts with one of these prefixes */
  folderPrefixes?: string[]
}

const defaultOptions: SoftwareUsedOptions = {
  folderPrefixes: ["1_Works"],
}

export default ((userOpts?: Partial<SoftwareUsedOptions>) => {
  const opts = { ...defaultOptions, ...userOpts }

  const SoftwareUsed: QuartzComponent = ({ fileData }: QuartzComponentProps) => {
    // Only render under specified folders
    const slug = fileData.slug ?? ""
    const isTarget = (opts.folderPrefixes ?? []).some(
      (prefix) => slug.startsWith(prefix + "/"),
    )
    if (!isTarget) return null

    // Skip index pages
    if (slug.endsWith("/index") || slug.endsWith("/")) return null

    const softwareList: string[] = (fileData.frontmatter as any)?.software ?? []
    if (softwareList.length === 0) return null

    return (
      <div class="software-used">
        <h4 class="software-used-title">Software Used</h4>
        <div class="software-used-list">
          {softwareList.map((key) => {
            const sw = SOFTWARE_MAP[key.toLowerCase()]
            const name = sw?.name ?? key
            const short = sw?.short ?? key.charAt(0).toUpperCase()
            const color = sw?.color ?? "#666"

            return (
              <span class="software-pill">
                <span class="software-icon" style={`background:${color}`}>
                  {short}
                </span>
                <span class="software-name">{name}</span>
              </span>
            )
          })}
        </div>
      </div>
    )
  }

  SoftwareUsed.css = style
  return SoftwareUsed
}) satisfies QuartzComponentConstructor
