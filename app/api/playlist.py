from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.playlist import Playlist
from app.models.playlist_song import PlaylistSong
from app.models.song import Song
from app.models.user import User
from app.schemas.playlist import (
    PlaylistCreate,
    PlaylistResponse,
    PlaylistSongCreate,
    PlaylistSongResponse
)
from app.schemas.song import SongResponse


router = APIRouter(
    prefix="/playlists",
    tags=["Playlists"]
)


def get_owned_playlist(
    playlist_id: int,
    user_id: int,
    db: Session
) -> Playlist:
    playlist = db.query(Playlist).filter(
        Playlist.playlist_id == playlist_id
    ).first()

    if playlist is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )

    if playlist.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to this playlist"
        )

    return playlist


@router.post("/", response_model=PlaylistResponse)
def create_playlist(
    playlist: PlaylistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_playlist = Playlist(
        name=playlist.name,
        description=playlist.description,
        user_id=current_user.user_id
    )

    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)

    return new_playlist


@router.get("/", response_model=list[PlaylistResponse])
def get_playlists(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Playlist).filter(
        Playlist.user_id == current_user.user_id
    ).offset((page - 1) * limit).limit(limit).all()


@router.get("/{playlist_id}", response_model=PlaylistResponse)
def get_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_owned_playlist(playlist_id, current_user.user_id, db)


@router.put("/{playlist_id}", response_model=PlaylistResponse)
def update_playlist(
    playlist_id: int,
    playlist_data: PlaylistCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    playlist = get_owned_playlist(playlist_id, current_user.user_id, db)
    playlist.name = playlist_data.name
    playlist.description = playlist_data.description

    db.commit()
    db.refresh(playlist)

    return playlist


@router.delete("/{playlist_id}")
def delete_playlist(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    playlist = get_owned_playlist(playlist_id, current_user.user_id, db)
    db.delete(playlist)
    db.commit()

    return {
        "message": "Playlist deleted successfully"
    }


@router.post(
    "/{playlist_id}/songs",
    response_model=PlaylistSongResponse
)
def add_song_to_playlist(
    playlist_id: int,
    song_data: PlaylistSongCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_owned_playlist(playlist_id, current_user.user_id, db)

    song = db.query(Song).filter(
        Song.song_id == song_data.song_id
    ).first()

    if song is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )

    existing_song = db.query(PlaylistSong).filter(
        PlaylistSong.playlist_id == playlist_id,
        PlaylistSong.song_id == song_data.song_id
    ).first()

    if existing_song is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Song is already in this playlist"
        )

    playlist_song = PlaylistSong(
        playlist_id=playlist_id,
        song_id=song_data.song_id
    )
    db.add(playlist_song)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Song is already in this playlist"
        )

    db.refresh(playlist_song)
    return playlist_song


@router.get("/{playlist_id}/songs", response_model=list[SongResponse])
def get_playlist_songs(
    playlist_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    playlist = get_owned_playlist(playlist_id, current_user.user_id, db)
    return [
        playlist_song.song
        for playlist_song in playlist.playlist_songs
    ]


@router.delete("/{playlist_id}/songs/{song_id}")
def remove_song_from_playlist(
    playlist_id: int,
    song_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    get_owned_playlist(playlist_id, current_user.user_id, db)

    playlist_song = db.query(PlaylistSong).filter(
        PlaylistSong.playlist_id == playlist_id,
        PlaylistSong.song_id == song_id
    ).first()

    if playlist_song is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song is not in this playlist"
        )

    db.delete(playlist_song)
    db.commit()

    return {
        "message": "Song removed from playlist successfully"
    }
