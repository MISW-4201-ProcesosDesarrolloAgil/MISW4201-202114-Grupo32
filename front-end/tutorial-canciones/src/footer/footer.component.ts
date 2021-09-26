import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-footer',
  templateUrl: './footer.component.html',
  styleUrls: ['./footer.component.css']
})
export class FooterComponent implements OnInit {

  constructor(
    private routerPath: Router,
    private router: ActivatedRoute) { }

  ngOnInit() {
  }

  goTo(menu: string) {
    const userId = parseInt(this.router.snapshot.params.userId)
    const token = this.router.snapshot.params.userToken
    if (menu === "about") {
      this.routerPath.navigate([`/about/${userId}/${token}`])
      console.log(":::userId", userId, ":::token", token);

    }
  }
  status: boolean = false;
  clickEvent() {
    this.status = !this.status;
  }
}
