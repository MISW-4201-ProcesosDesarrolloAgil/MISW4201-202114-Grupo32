export class Cancion {
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
    }
}
