export class Album {
    private es_compartido: boolean;
    constructor(
        public id: number,
        public titulo: string,
        public anio: number,
        public descripcion: string,
        public medio: Medio,
        public usuario: number,
        public interpretes: Array<string>,
        public canciones: Array<Cancion>,
        public compartido_a: Array<number>
    ){
        this.id = id;
        this.titulo = titulo;
        this.anio = anio;
        this.descripcion = descripcion;
        this.medio = medio;
        this.usuario = usuario;
        this.interpretes = interpretes;
        this.canciones = canciones;
        this.compartido_a = compartido_a;
        this.es_compartido = false;
    }
}

export class Medio{
    llave: string;
    valor: number

    constructor(
        llave: string,
        valor:number
    ){
        this.llave = llave;
        this.valor = valor;
    }
}

export class Cancion{
    id: number;
    titulo: string;
    minutos: number;
    segundos: number;
    interprete: string;

    constructor(
        id: number,
        titulo: string,
        minutos: number,
        segundos: number,
        interprete: string
    ){
        this.id = id;
        this.titulo = titulo;
        this.minutos = minutos;
        this.segundos = segundos;
        this.interprete = interprete;
    }
}

export class AlbumCompartido extends Album{
  constructor(
    public id: number,
    public titulo: string,
    public anio: number,
    public descripcion: string,
    public medio: Medio,
    public usuario: number,
    public interpretes: Array<string>,
    public canciones: Array<Cancion>,
    public compartido_a: Array<number>,
    public nombre_dueno: String){
      super(id, titulo, anio, descripcion, medio, usuario, interpretes, canciones, compartido_a)
  }
}

export class Comentario{
  comentario: string;
  fecha: string;
  usuario_id: number;
  album_id: number;
  nombre_usuario?:string;

  constructor(
    comentario: string,
    fecha: string,
    usuario_id: number,
    album_id: number,
  ){
      this.comentario = comentario;
      this.fecha = fecha;
      this.usuario_id = usuario_id;
      this.album_id = album_id;
  }
}
