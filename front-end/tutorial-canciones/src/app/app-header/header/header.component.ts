import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import * as $ from 'jquery';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  constructor(
    private routerPath: Router,
    private router: ActivatedRoute
  ) { }

  ngOnInit(): void {
    // $('#sidebarCollapse').on('click', function () {
    //   $('#sidebar, #content').toggleClass('active');
    // });
    $(document).ready(function () {
      $("#sidebarCollapse").on('click', function () {
        $("#sidebar").toggleClass('active');
      });
    });
  }

  goTo(menu: string) {
    const userId = parseInt(this.router.snapshot.params.userId)
    const token = this.router.snapshot.params.userToken
    if (menu === "logIn") {
      this.routerPath.navigate([`/`])
    }
    else if (menu === "home") {
      this.routerPath.navigate([`/home/${userId}/${token}`])
    }
    else if (menu === "album") {
      this.routerPath.navigate([`/albumes/${userId}/${token}`])
    }
    else if (menu === "cancion") {
      this.routerPath.navigate([`/canciones/${userId}/${token}`])
    }
    else if (menu === "about") {
      this.routerPath.navigate([`/about/${userId}/${token}`])
    }
  }

  status: boolean = false;
  clickEvent() {
    this.status = !this.status;
  }

}
