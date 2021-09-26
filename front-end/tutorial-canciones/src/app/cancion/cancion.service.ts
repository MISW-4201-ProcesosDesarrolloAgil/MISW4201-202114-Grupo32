import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cancion,CancionCompartida } from './cancion';
import { Album } from '../album/album';

@Injectable({
  providedIn: 'root'
})
export class CancionService {

  private backUrl: string = "http://localhost:5000"

  constructor(private http: HttpClient) { }

  getCancionesAlbum(idAlbum: number, token: string): Observable<Cancion[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Cancion[]>(`${this.backUrl}/album/${idAlbum}/canciones`, {headers: headers})
  }

  getCanciones(id_usuario: number, token: string): Observable<Cancion[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<Cancion[]>(`${this.backUrl}/canciones/usuario/${id_usuario}`, {headers: headers})
  }

  getCancionesCompartidas(id_usuario: number, token: string): Observable<CancionCompartida[]>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.get<CancionCompartida[]>(`${this.backUrl}/usuario/${id_usuario}/canciones_compartidas`, {headers: headers})
  }

  getAlbumesCancion(cancionId: number): Observable<Album[]>{
    return this.http.get<Album[]>(`${this.backUrl}/cancion/${cancionId}/albumes`)
  }

  crearCancion( id_usuario: number, cancion: Cancion, token: string):Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.post<Cancion>(`${this.backUrl}/canciones/usuario/${id_usuario}`, cancion, {headers: headers})
  }

  getCancion(cancionId: number): Observable<Cancion>{
    return this.http.get<Cancion>(`${this.backUrl}/cancion/${cancionId}`)
  }

  editarCancion(cancion: Cancion, cancionId: number, token: string):Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.put<Cancion>(`${this.backUrl}/cancion/${cancionId}`, cancion, {headers: headers})
  }

  eliminarCancion(cancionId: number, token: string): Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.delete<Cancion>(`${this.backUrl}/cancion/${cancionId}`, {headers: headers})
  }

  compartirCancion(token:string, cancion: Cancion, usuarios: Array<number>): Observable<Cancion>{
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${token}`
    })
    return this.http.post<Cancion>(`${this.backUrl}/compartir/cancion/${cancion.id}`, {"id_usuarios": usuarios}, {headers: headers})
  }

}
