import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { HomeComponent } from './home.component';
import { AppHeaderModule } from '../app-header/app-header.module';


@NgModule({
  declarations: [HomeComponent],
  imports:  [
    CommonModule, AppHeaderModule, ReactiveFormsModule
  ],
  exports: [HomeComponent]
})
export class HomeModule { }
