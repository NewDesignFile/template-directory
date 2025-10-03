from playwright.sync_api import sync_playwright, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("http://localhost:4321")

    # Verify Phasmophobia Sound Recorder in Audio
    page.get_by_label("Navigate to Audio category with").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("http://localhost:4321/categories/audio")
    page.wait_for_selector("text=Phasmophobia Sound Recorder")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.screenshot(path="jules-scratch/verification/audio-category.png")

    # Verify AI Photo Editor in Photos
    page.get_by_label("Navigate to Photos category with").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("http://localhost:4321/categories/photos")
    page.wait_for_selector("text=AI Photo Editor")
    page.screenshot(path="jules-scratch/verification/photos-category-1.png")

    # Verify Ghostface AI in Photos
    page.wait_for_selector("text=Ghostface AI")
    page.screenshot(path="jules-scratch/verification/photos-category-2.png")

    # Verify SilentSalt in Gaming
    page.get_by_label("Navigate to Gaming category with").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("http://localhost:4321/categories/gaming")
    page.wait_for_selector("text=SilentSalt")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.screenshot(path="jules-scratch/verification/gaming-category.png")

    # Verify Seedances in Video
    page.get_by_label("Navigate to Video category with").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("http://localhost:4321/categories/video")
    page.wait_for_selector("text=Seedances")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.screenshot(path="jules-scratch/verification/video-category.png")

    # Verify Fluxaicreate in Xtras
    page.get_by_label("Navigate to Xtras category with").click()
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url("http://localhost:4321/categories/xtras")
    page.wait_for_selector("text=Fluxaicreate")
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.screenshot(path="jules-scratch/verification/xtras-category.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)