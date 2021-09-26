import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http'
import { ToastrModule } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UsuarioModule } from './usuario/usuario.module';
import { AlbumModule } from './album/album.module';
import { AppHeaderModule } from './app-header/app-header.module';
import { CancionModule } from './cancion/cancion.module';
import { HomeModule } from './home/home.module';
import { AboutModule } from './about/about.module';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { FooterComponent } from '../footer/footer.component';

@NgModule({
  declarations: [
    AppComponent,
    FooterComponent
   ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    HomeModule,
    AboutModule,
    UsuarioModule,
    AlbumModule,
    CancionModule,
    AppHeaderModule,
    ToastrModule.forRoot({
      timeOut: 7000,
      positionClass: 'toast-bottom-right',
      preventDuplicates: true,
    }),
    BrowserAnimationsModule,
    NgbModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
