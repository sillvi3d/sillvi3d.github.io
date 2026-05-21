import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://sillvi3d.github.io/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Sillvi's Second Brain",
    pageTitleSuffix: "",
    enableSPA: false,
    enablePopovers: true,
    analytics: {
      provider: "google",
      tagId: "G-WQ8EMEECF3",
    },
    locale: "en-US",
    baseUrl: "sillvi3d.github.io",
    head: [
      {
        tag: "meta",
        attrs: {
          name: "google-site-verification",
          content: "a2lsjTo72JaTNWz3dQ6uZjoMqrOWGmyCdFPiwOEMLUM",
        },
      },
    ],
    ignorePatterns: [
      // ── 현재(구) 폴더명 ──
      "0. 202x/**",
      "1. About Me/**",
      "3. SW information/**",
      "3. SW 도감/**",
      "3. 강의/**",
      "4. 배경 모델러/**",
      "5. 독서/**",
      "5. 미디어/**",
      "6. Side projects/**",
      "6. 회사/**",
      "9. 서식/**",
      "9. 잡정보/**",
      // "99. 이미지 파일들/**",  // 이미지는 quartz가 접근 필요 — 제외하지 않음
      "99. json/**",
      "output/**",
      "scripts/**",
      "custom instruction/**",
      "_Templates/**",
      "_Meta/**",
      "_config/**",
      // ── 새 폴더명 (Phase 1 이후) ──
      "0_Inbox/**",
      "5_Project/**",
      "6_Work/**",
      "7_Life/**",
      "_Template/**",
      "_Config/**",
      "_Script/**",
      "_Instruction/**",
      // "_Attachment/**",  // 이미지는 quartz가 접근 필요 — 제외하지 않음
      // ── 시스템 ──
      ".obsidian/**",
      ".git/**",
      "private",
      "templates",
    ],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Inter",
        body: "Inter",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#ffffff",
          lightgray: "#f0f0f0",
          gray: "#b8b8b8",
          darkgray: "#4e4e4e",
          dark: "#1a1a1a",
          secondary: "#3d7a5e",
          tertiary: "#5aab85",
          highlight: "rgba(61, 122, 94, 0.1)",
          textHighlight: "#b3f5d088",
        },
        darkMode: {
          light: "#1a1a1a",
          lightgray: "#2a2a2a",
          gray: "#555555",
          darkgray: "#d4d4d4",
          dark: "#ebebec",
          secondary: "#5aab85",
          tertiary: "#3d7a5e",
          highlight: "rgba(90, 171, 133, 0.15)",
          textHighlight: "#3d7a5e88",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      Plugin.CustomOgImages(),
    ],
  },
}

export default config