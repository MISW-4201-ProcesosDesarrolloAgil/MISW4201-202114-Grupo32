export class UsuarioSimple{
  id: number;
  nombre: string;
  constructor(
    id: number,
    nombre: string
  ){
    this.id = id;
    this.nombre = nombre;
  }
}

export class Usuario extends UsuarioSimple{
    albumes: Array<any>
    constructor(
        id: number,
        nombre: string,
        albumes: Array<any>,
    ){
        super(id, nombre);
        this.albumes = albumes
    }
}
