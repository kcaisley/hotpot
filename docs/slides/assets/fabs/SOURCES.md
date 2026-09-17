# Foundries and cross-section sources

- Retrieved 2026-09-17. Logos retain their original colors and identify their respective organizations.
- Map: [BlankMap-World.svg](https://commons.wikimedia.org/wiki/File:BlankMap-World.svg), Canuckguy and contributors, public domain. `world.svg` is the source; `world-nord.svg` changes land to Nord gray. Markers indicate cities at world-map scale.
- SkyWater photo: [SkyWater Building Exterior](https://commons.wikimedia.org/wiki/File:SkyWater_Building_Exterior.jpg), Iceone2000, 2021, [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Uncropped, scaled only; original resolution is 360 × 194 pixels.
- SkyWater logo: https://www.skywatertechnology.com/wp-content/uploads/2022/01/skywater-logo.svg
- IHP aerial photo: https://www.ihp-microelectronics.com/fileadmin/user_upload/DJI_0789.JPG — official IHP website, © IHP; scaled only. No open license asserted.
- IHP logo: https://www.ihp-microelectronics.com/_assets/07f43f764fd345573d01c3fa61ab86d5/Images/IHP-Logo-ohne-claim.svg — official IHP website.
- GF Singapore campus photo: [Singapore manufacturing](https://gf.com/manufacturing/singapore/), © GlobalFoundries, scaled only. Direct asset: https://assets.gf.com/image/328833518282/image_qavuoo53pt7lpfdttqvqih1r0c/-B1920-FWEBP . This is a campus illustration; it does not establish the current GF180MCU production building. No open license asserted.
- GF logo: original inline SVG from the header of the same official Singapore manufacturing page.
- Company logos remain the property/trademarks of their respective owners; they are not relicensed with the deck.

## Process and location references

- [SkyWater open PDK](https://github.com/google/skywater-pdk); [Minnesota 130 nm manufacturing context](https://www.skywatertechnology.com/?p=5395).
- [IHP SG13G2 open PDK](https://github.com/IHP-GmbH/IHP-Open-PDK); [IHP open-source fabrication service](https://dk.ihp-microelectronics.com/OpenSourceRequest.php); IHP is in Frankfurt (Oder), Germany.
- [GF180MCU specification](https://gf180mcu-pdk.readthedocs.io/en/latest/analog/layout/inter_specs/inter_specs.html) names GlobalFoundries Singapore and the legacy FAB3E technology.
- [wafer.space GF180MCU fabrication](https://www.crowdsupply.com/wafer-space/gf180mcu-run-3) explicitly identifies fabrication at GlobalFoundries in Singapore.
- Open PDK availability is distinct from free fabrication or unrestricted production qualification; shuttle/service access is separate.

## CMOS cross-section illustration

- [Cmos-chip structure in 2000s (en).svg](https://commons.wikimedia.org/wiki/File:Cmos-chip_structure_in_2000s_(en).svg), Cepheiden, 9 December 2006.
- Used under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/); the source also offers GFDL and CC BY 2.5.
- `../cmos-cross-section.svg` is the original multilingual SVG. Render with `rsvg-convert --accept-language=en` to select English. `prepare_cmos.py` removes the material legend and renders the English illustration to PDF. The adapted illustration retains CC BY-SA 3.0.
- General early-2000s CMOS-on-SOI illustration with five metallization levels and a solder bump; not the DMC65 or Nangate45 process cross section.
- A compact source hyperlink appears in the slide footer; full author/license attribution remains here and in speaker notes.

## DMC65 layout

- Local source: `~/Documents/asiclab/projects/dmc65/dmc65_web.webp`.
- Copied as `../dmc65-layout.webp`; converted to PNG for LaTeX without cropping or retouching.
- Existing ArtistIC layout rendering; shows bump-pad locations, not physical solder bumps.
- Project provenance: `~/Documents/asiclab/projects/dmc65/provenance.md`, DMC65v1/dmc_top/layout revision 4 (13 June 2022), 2.9 × 4.8 mm die.
