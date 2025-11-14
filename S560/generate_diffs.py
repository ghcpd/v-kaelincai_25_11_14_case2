from PIL import Image, ImageChops
from pathlib import Path

root = Path('.').resolve()
pre_dir = root/'Project_A_BaselineUI'/'screenshots'
post_dir = root/'Project_B_ImprovedUI'/'screenshots'
diff_dir = root/'results'/'diffs'
diff_dir.mkdir(parents=True, exist_ok=True)

pairs = [
    ('screenshot_pre_ui.png','screenshot_post_ui.png'),
    ('screenshot_pre_spacing_hierarchy.png','screenshot_post_spacing_hierarchy.png'),
    ('screenshot_pre_button_hover.png','screenshot_post_button_hover.png'),
    ('screenshot_pre_icon_consistency.png','screenshot_post_icon_consistency.png')
]

for a,b in pairs:
    pa = pre_dir/a
    pb = post_dir/b
    if pa.exists() and pb.exists():
        im1 = Image.open(pa).convert('RGBA')
        im2 = Image.open(pb).convert('RGBA')
        if im1.size != im2.size:
            # create equal size by resizing second
            im2 = im2.resize(im1.size)
        diff = ImageChops.difference(im1,im2)
        out = diff_dir/f"diff_{a.replace('screenshot_pre_','')}.png"
        diff.save(out)
        print('Saved',out)
    else:
        print('Missing pair',pa,pb)
