import { TestBed, getTestBed, inject } from '@angular/core/testing';

import {
  HttpTestingController,
  HttpClientTestingModule,
} from '@angular/common/http/testing';

import { AlbumService } from './album.service';
import { environment } from 'src/environments/environment';
import { Album, Comentario, Medio } from './album';
import * as faker from 'faker'

describe('Service: Album', () => {
  let injector: TestBed;
  let service: AlbumService;
  let httpMock: HttpTestingController;
  let apiUrl = environment.apiUrl;
  let medios:Array<Medio> = [
    {
      llave: "DISCO",
      valor: 1
    },
    {
      llave: "CASETE",
      valor: 2
    },
    {
      llave: "CD",
      valor: 3
    }
  ]

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AlbumService]
    });

    injector = getTestBed();
    service = injector.get(AlbumService);
    httpMock = injector.get(HttpTestingController);
  });

  it('should create service', inject([AlbumService], (service: AlbumService) => {
    expect(service).toBeTruthy();
  }));

  afterEach(() => {
    httpMock.verify();
  });

  it('compartirAlbum() should be correct', () => {
    let mokPosts = new Album(faker.datatype.number(), faker.lorem.sentence(),2000, faker.lorem.sentence(), medios[0], 1,[],[],[1,2,3]);

    let token = faker.datatype.uuid();
    let usuarios = [2,3,4]

    service.compartirAlbum(token, mokPosts, usuarios).subscribe(album => {
      expect(album).toBeInstanceOf(Album);
    });

    const req = httpMock.expectOne(`${apiUrl}/compartir/album/${mokPosts.id}`);
    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get("Authorization")).toBe(`Bearer ${token}`);
    let givenUserList = req.request.body.id_usuarios
    expect(givenUserList.length).toBe(usuarios.length)
    for(let i = 0; i < usuarios.length; i++){
      expect(givenUserList[i]).toBe(usuarios[i]);
    }

    req.flush(mokPosts);
  });

  it('enviarComentario()', () => {

    let token = faker.datatype.uuid();
    let usuarios = [1,2]
    let albums = [1,2]
    let comentario = faker.lorem.words(10);
    let fecha = new Date();

    let mockComentario: Comentario = new Comentario(comentario, fecha.toISOString() , usuarios[0], albums[0]  );


    service.enviarComentario(token, mockComentario).subscribe(comentario => {
      expect(comentario).toBeInstanceOf(Comentario);
    });

    const req = httpMock.expectOne(`${apiUrl}/album/${mockComentario.album_id}/comentario`);
    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get("Authorization")).toBe(`Bearer ${token}`);
    req.flush(mockComentario);
  });

});
