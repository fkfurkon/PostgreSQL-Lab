import flask

import models
import forms
from flask_wtf import FlaskForm


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)


@app.route("/")
def index():
    db = models.db
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.title)
    ).scalars()
    delete_form = DeleteForm()
    return flask.render_template(
        "index.html",
        notes=notes,
        delete_form=delete_form 
    )


@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if not form.validate_on_submit():
        print("error", form.errors)
        return flask.render_template(
            "notes-create.html",
            form=form,
        )
    note = models.Note()
    form.populate_obj(note)
    note.tags = []

    db = models.db
    for tag_name in form.tags.data:
        tag = (
            db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
            .scalars()
            .first()
        )

        if not tag:
            tag = models.Tag(name=tag_name)
            db.session.add(tag)

        note.tags.append(tag)

    db.session.add(note)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))


@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    db = models.db
    tag = (
        db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
        .scalars()
        .first()
    )
    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars()

    return flask.render_template(
        "tags-view.html",
        tag_name=tag_name,
        notes=notes,
    )

@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def note_edit(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)

    form = forms.NoteForm(obj=note)

    if form.validate_on_submit():
        # กรอก field ปกติ ยกเว้น tags
        for field_name in form._fields:
            if field_name != "tags":
                setattr(note, field_name, form._fields[field_name].data)

        # จัดการ tags แยกต่างหาก
        note.tags = []
        for tag_name in form.tags.data:
            tag = db.session.execute(
                db.select(models.Tag).where(models.Tag.name == tag_name)
            ).scalars().first()
            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)
            note.tags.append(tag)

        db.session.commit()
        return flask.redirect(flask.url_for("index"))

    else:
        # ดึงชื่อ tag เพื่อแสดงใน form
        form.tags.data = [tag.name for tag in note.tags]

    return flask.render_template("note-edit.html", form=form, note=note)

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def note_delete(note_id):
    db = models.db
    note = db.session.get(models.Note, note_id)
    if not note:
        flask.abort(404)

    db.session.delete(note)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))

# delete tags
@app.route("/tags/<tag_name>/delete", methods=["POST"])
def tag_delete(tag_name):
    db = models.db
    tag = (
        db.session.execute(db.select(models.Tag).where(models.Tag.name == tag_name))
        .scalars()
        .first()
    )
    if not tag:
        flask.abort(404)

    # Remove the tag from all notes
    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars()
    for note in notes:
        note.tags.remove(tag)

    # Delete the tag itself
    db.session.delete(tag)
    db.session.commit()

    return flask.redirect(flask.url_for("index"))

class DeleteForm(FlaskForm):
    pass


if __name__ == "__main__":
    app.run(debug=True)
