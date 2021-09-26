export class Cancion {
    private es_compartido: boolean;
    constructor(
        public id: number,
        public titulo: string,
        public minutos: number,
        public segundos: number,
        public interprete: string,
        public albumes: Array<any>,
        public usuario: number,
        public compartido_a: Array<number>
    ){
      this.id= id;
      this.titulo= titulo;
      this.minutos= minutos;
      this.segundos= segundos;
      this.interprete= interprete;
      this.albumes= albumes;
      this.usuario= usuario;
      this.compartido_a= compartido_a;
      this.es_compartido = false;
    }
}


export class CancionCompartida extends Cancion{
  constructor(
    public id: number,
    public titulo: string,
    public minutos: number,
    public segundos: number,
    public interprete: string,
    public albumes: Array<any>,
    public usuario: number,
    public compartido_a: Array<number>,
    public nombre_dueno: String){
      super(id, titulo, minutos, segundos, interprete, albumes, usuario, compartido_a)
  }
}
