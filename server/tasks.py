from invoke import task


@task
def build(ctx):
    ctx.run("pyinstaller -F --hidden-import main main.py")
