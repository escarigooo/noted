# Asset provenance

Last reviewed: 2026-08-31

Only the files listed here are approved for publication. The previous image/font set had unknown provenance and was removed in issue #4. The publication history was rewritten on 2026-08-31 to remove those historical files; see `HISTORY_REWRITE.md`. The repository remains private pending GitHub-side cleanup of legacy pull-request references and cached views.

## AI-generated catalogue images

The four PNGs below were generated specifically for Noted with OpenAI's built-in image generation tool on 2026-08-31. No existing repository image or other input image was supplied as a reference. André Escarigo selected and reviewed the outputs and is responsible for their use. OpenAI's terms state that, as between the user and OpenAI and to the extent permitted by law, the user owns output; outputs may not be unique and users remain responsible for evaluating them: https://openai.com/policies/terms-of-use/

The prompts required original fictional industrial designs and explicitly excluded text, logos, trademarks, watermarks, and resemblance to named commercial products.

| File | Purpose | SHA-256 |
|---|---|---|
| `noted/static/img/products/tablet.png` | fictional digital-paper tablet and stylus | `46f9935c1a4f7cb0b13a76befb253e10ffc22bef6826aadabdcfb9176ed59aac` |
| `noted/static/img/products/stylus.png` | fictional stylus and replacement nibs | `7fab78889842d4f73d58e9e6a83268ad771c809c0f5539f386c65bc26d7deb89` |
| `noted/static/img/products/folio.png` | fictional keyboard folio | `ccaac9a6e6a6def0bda0bd92c6d5ae47749d18d9bcace031a4497c9f040e3771` |
| `noted/static/img/products/essentials.png` | generic cable, sleeve, and planner | `50e6f94b75a09d3c61bb04b5466e56b6be2c801d2e542f9ccf6a3d0b2528146b` |

### Final prompt set

All prompts used `product-mockup`, a square catalogue composition, a warm off-white studio background, soft diffused light, graphite/warm-white/mustard palette, and these constraints: entirely original generic design; no text, logos, trademarks, watermark, hands, or packaging; avoid resemblance to identifiable commercial products.

- Tablet: “an original generic digital paper notebook tablet with a slim stylus resting beside it”; blank paper-like screen, matte recycled polymer and anodized stylus.
- Stylus: “an original generic digital writing stylus with three small replacement nibs”; exactly one stylus and three aligned nibs.
- Folio: “an original generic keyboard folio for a digital paper notebook tablet”; blank keys and an empty support panel in recycled woven fabric.
- Essentials: “an original generic desk accessory set for digital note-taking”; exactly one coiled USB-C cable, one protective sleeve, and one blank recycled-paper planner.

## Repository-authored SVG assets

`logo.svg`, `logo-mark.svg`, the seven navigation icons, the four category illustrations, and `products/placeholder.svg` were authored directly as simple SVG markup for this repository on 2026-08-31. They contain only geometric shapes and system-font text. They are covered by the repository MIT licence.

## Fonts

No font file is redistributed. CSS uses local system font stacks. A browser may render a different available font per operating system; no external font download is required.

## Runtime browser assets

Chart.js 4.5.1 is loaded from jsDelivr for the experimental admin analytics page. It is third-party MIT-licensed code, documented in `THIRD_PARTY_NOTICES.md`; it is not a repository-authored visual asset. No remote font or flag image is loaded.

## Third-party brands and marks

No third-party logos or payment marks are intentionally included. The catalogue names and products are fictional. Links to GitHub identify the developer/platform and do not imply endorsement.
