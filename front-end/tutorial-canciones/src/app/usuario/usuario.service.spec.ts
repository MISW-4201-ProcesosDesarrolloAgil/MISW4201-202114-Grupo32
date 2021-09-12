/* tslint:disable:no-unused-variable */

import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed, async, inject, getTestBed } from '@angular/core/testing';
import { environment } from 'src/environments/environment';
import { Usuario } from './usuario';
import { UsuarioService } from './usuario.service';
import * as faker from 'faker'

const numberOfUsers: number = 10

describe('Service: Usuario', () => {
  let injector: TestBed;
  let service: UsuarioService;
  let httpMock: HttpTestingController;
  let apiUrl = environment.apiUrl;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UsuarioService]
    });

    injector = getTestBed();
    service = injector.get(UsuarioService);
    httpMock = injector.get(HttpTestingController);
  });

  it('should create service', inject([UsuarioService], (service: UsuarioService) => {
    expect(service).toBeTruthy();
  }));

  afterEach(() => {
    httpMock.verify();
  });

  it(`getUsuarios() should return ${numberOfUsers} users`, () => {
    let mokPosts: Usuario[] = [];
    for (let i = 0; i < numberOfUsers; i++){
      mokPosts.push( new Usuario(
        i,
        faker.name.findName(),
        []
      ));
    }

    let token = faker.datatype.uuid();

    service.getUsuarios(token).subscribe(usuario => {
      expect(usuario.length).toBe(numberOfUsers);
    });

    const req = httpMock.expectOne(apiUrl + "/usuarios");
    expect(req.request.method).toBe('GET');
    expect(req.request.headers.get("Authorization")).toBe(`Bearer ${token}`);
    req.flush(mokPosts);
  })
});
