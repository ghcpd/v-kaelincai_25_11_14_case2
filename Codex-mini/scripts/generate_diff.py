from pathlib import Path
from PIL import Image, ImageChops

PRE = Path('Project_A_BaselineUI/screenshots/screenshot_pre_ui.png')
POST = Path('Project_B_ImprovedUI/screenshots/screenshot_post_ui.png')
DEST = Path('results/diff_ui.png')
DEST.parent.mkdir(parents=True, exist_ok=True)
pre = Image.open(PRE).convert('RGBA')
post = Image.open(POST).convert('RGBA')
if pre.size != post.size:
    max_w = max(pre.width, post.width)
    max_h = max(pre.height, post.height)
    canvas_pre = Image.new('RGBA', (max_w, max_h), (255, 255, 255, 255))
    canvas_post = Image.new('RGBA', (max_w, max_h), (255, 255, 255, 255))
    canvas_pre.paste(pre, (0, 0))
    canvas_post.paste(post, (0, 0))
    pre, post = canvas_pre, canvas_post
diff = ImageChops.difference(pre, post)
mask = diff.convert('L').point(lambda x: 255 if x > 15 else 0)
highlight = Image.new('RGBA', pre.size, (255, 63, 63, 120))
result = Image.composite(highlight, post, mask)
result.save(DEST)
