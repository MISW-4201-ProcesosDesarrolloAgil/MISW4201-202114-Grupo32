import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Album, AlbumCompartido, Comentario } from './album';
import { Cancion } from '../cancion/cancion';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AlbumService {

  private backUrl: string = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getAlbumes(usuario: number, token: string): Observable<Album[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Album[]>(`${this.backUrl}/usuario/${usuario}/albumes`, { headers: headers })
  }

  getAlbumesCompartidos(usuario: number, token: string): Observable<AlbumCompartido[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<AlbumCompartido[]>(`${this.backUrl}/usuario/${usuario}/albumes_compartidos`, { headers: headers })
  }

  getCancionesAlbum(idAlbum: number, token: string): Observable<Cancion[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Cancion[]>(`${this.backUrl}/album/${idAlbum}/canciones`, { headers: headers })
  }

  crearAlbum(idUsuario: number, token: string, album: Album): Observable<Album> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.post<Album>(`${this.backUrl}/usuario/${idUsuario}/albumes`, album, { headers: headers })
  }

  getAlbum(albumId: number): Observable<Album> {
    return this.http.get<Album>(`${this.backUrl}/album/${albumId}`)
  }

  editarAlbum(idUsuario: number, token: string, albumId: number, album: Album): Observable<Album> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.put<Album>(`${this.backUrl}/album/${albumId}`, album, { headers: headers })
  }

  eliminarAlbum(idUsuario: number, token: string, albumId: number): Observable<Album> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.delete<Album>(`${this.backUrl}/album/${albumId}`, { headers: headers })
  }

  asociarCancion(albumId: number, cancionId: number): Observable<Cancion> {
    return this.http.post<Cancion>(`${this.backUrl}/album/${albumId}/canciones`, { "id_cancion": cancionId })
  }

  compartirAlbum(token: string, album: Album, usuarios: Array<number>): Observable<Album> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.post<Album>(`${this.backUrl}/compartir/album/${album.id}`, { "id_usuarios": usuarios }, { headers: headers })
  }

  getComentario(albumId: number, token: string): Observable<Comentario[]> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Comentario[]>(`${this.backUrl}/album/${albumId}/comentario`, { headers: headers })
  }

  enviarComentario(token: string, comentario: Comentario): Observable<Comentario> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.post<Comentario>(`${this.backUrl}/album/${comentario.album_id}/comentario`, comentario , { headers: headers })
  }


}
