import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { AppHeaderModule } from '../app-header/app-header.module';
import { AboutComponent } from './about.component';


@NgModule({
  declarations: [AboutComponent],
  imports:  [
    CommonModule, AppHeaderModule, ReactiveFormsModule
  ],
  exports: [AboutComponent]
})
export class AboutModule { }
