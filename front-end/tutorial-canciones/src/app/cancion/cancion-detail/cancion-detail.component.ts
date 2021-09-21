import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Cancion } from '../cancion';
import { UsuarioSimple } from 'src/app/usuario/usuario';
import { CancionService } from '../cancion.service';
import { UsuarioService } from 'src/app/usuario/usuario.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-cancion-detail',
  templateUrl: './cancion-detail.component.html',
  styleUrls: ['./cancion-detail.component.css']
})
export class CancionDetailComponent implements OnInit {

  @Input() cancion: Cancion;
  @Output() deleteCancion = new EventEmitter();

  userId: number;
  token: string;
  userList: Array<UsuarioSimple>;
  usuariosACompartir: Array<number>

  constructor(
    private router: ActivatedRoute,
    private routerPath: Router,
    private toastr: ToastrService,
    private cancionService: CancionService,
    private usuarioService: UsuarioService,
  ) { }

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId)
    this.token = this.router.snapshot.params.userToken

  }

  eliminarCancion(){
    this.deleteCancion.emit(this.cancion.id)
  }

  goToEdit(){
    this.routerPath.navigate([`/canciones/edit/${this.cancion.id}/${this.userId}/${this.token}`])
  }

  compartirCancion(){
    this.usuarioService.getUsuarios(this.token).subscribe(usuarios => {
      this.userList = usuarios.filter( user => {
        return user.id != this.cancion.usuario && this.cancion.compartido_a.indexOf(user.id) == -1;
      })
    })
    this.usuariosACompartir = []
  }

  onSubmitCompartirCancion(){
    if (this.usuariosACompartir.length > 0)
    {
      this.cancionService.compartirCancion(this.token, this.cancion, this.usuariosACompartir).subscribe(cancion => {
        cancion.usuario = this.cancion.usuario;
        this.cancion = cancion;
        console.log(cancion);
        this.albumCompartidoExitosamente()
      }, error => {
        this.showError("Hubo un error. ->" + error.message)
      })
    }else{
      this.showError("Debe seleccionar al menos un usuario para compartir.")
    }
  }

  onCheckboxChange(event: any){
    if (event.target.checked){
      this.usuariosACompartir.push(parseInt(event.target.value));
    }else{
      let value = parseInt(event.target.value);
      this.usuariosACompartir = this.usuariosACompartir.filter( userId => userId != value);
    }
    console.log(this.usuariosACompartir)
  }

  showError(error: string){
    this.toastr.error(error, "Error")
  }

  showWarning(warning: string){
    this.toastr.warning(warning, "Error de autenticación")
  }

  albumCompartidoExitosamente() {
    this.toastr.success(`La cancion "${this.cancion.titulo}" fue compartido.`, "Actualización exitosa");
  }


}
