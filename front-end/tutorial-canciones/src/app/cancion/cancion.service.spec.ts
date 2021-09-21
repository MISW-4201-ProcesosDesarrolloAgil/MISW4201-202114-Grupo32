/* tslint:disable:no-unused-variable */

import { HttpTestingController, HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed, async, inject, getTestBed } from '@angular/core/testing';
import { CancionService } from './cancion.service';
import { environment } from 'src/environments/environment';
import * as faker from 'faker'
import { Cancion } from '../cancion/cancion';

describe('Service: Cancion', () => {
  let injector: TestBed;
  let service: CancionService;
  let httpMock: HttpTestingController;
  let apiUrl = environment.apiUrl;
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CancionService]
    });
    injector = getTestBed();
    service = injector.get(CancionService);
    httpMock = injector.get(HttpTestingController);
  });

  it('should create service', inject([CancionService], (service: CancionService) => {
    expect(service).toBeTruthy();
  }));

  afterEach(() => {
    httpMock.verify();
  });

  it('compartirCancion() should be correct', ()=>{
    let mokPosts = new Cancion(faker.datatype.number(), faker.lorem.sentence(), 3, 20, faker.name.firstName(), [], 1, [])
    let token = faker.datatype.uuid();
    let usuarios = [2,3,4]
    service.compartirCancion(token, mokPosts, usuarios).subscribe(cancion => {
      expect(cancion).toBeInstanceOf(Cancion);
    });

    const req = httpMock.expectOne(`${apiUrl}/compartir/cancion/${mokPosts.id}`);
    expect(req.request.method).toBe('POST');
    expect(req.request.headers.get("Authorization")).toBe(`Bearer ${token}`);
    let givenUserList = req.request.body.id_usuarios
    expect(givenUserList.length).toBe(usuarios.length)
    for(let i = 0; i < usuarios.length; i++){
      expect(givenUserList[i]).toBe(usuarios[i]);
    }

    req.flush(mokPosts);
  });

});
