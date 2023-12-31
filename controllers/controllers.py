# -*- coding: utf-8 -*-
import logging
import werkzeug

from odoo import http
from odoo.http import request

class StripeLinkController(http.Controller):

    @http.route('/payment/stripe/reauth', type='http', auth='none')
    def stripe_refresh_account_link(self,**kwargs):
        data = kwargs.copy()
        old_link = request.env['res.partner'].sudo().search([('id', '=', data['partner_id'])]).stripe_connect_account_link
        link = request.env['res.partner'].sudo().search([('id', '=', data['partner_id'])]).generate_stripe_connect_account_link(data['account_id'], data['reauth_url'], data['return_url'])
        if (link):
            return werkzeug.utils.redirect(link.get('url'))
        else:
            return """
            <!DOCTYPE html>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                .contenedor {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%%;
                    height: 100%%;
                    justify-content: center !important;
                }

                .logo {
                    padding-top: 22%%;
                    width: 43%%;
                    height: 43%%;
                }

                .correcto {
                    font-size: 1.8vw;
                    padding-top: 45%%
                }

                .tex {
                    font-size: 1.1vw;
                }

                .boton {
                    width: 10%%;
                    height: 33px;
                    margin-top: 95px;
                    background-color: rgb(246, 183, 118);
                    border-radius: 5px 5px 5px 5px;
                    color: rgb(0, 0, 0);
                    border: 1px solid rgba(246, 183, 118, 0.22) !important;
                }


                @media only screen and (max-width: 576px) {

                    /* For mobile phones: */
                    .contenedor {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        width: 100%%;
                        height: 100%%;
                        justify-content: center !important;
                    }

                    .logo {
                        padding-top: 38%%;
                        width: 33%%;
                        height: 33%%;
                    }

                    .correcto {
                        font-size: 5.3vw;
                        margin-bottom: 10px;
                    }

                    .tex {
                        font-size: 3.2vw;
                    }

                    .boton {
                        width: 28%%;
                        height: 40px;
                        margin-top: 95px;
                        background-color: rgb(246, 183, 118);
                        border-radius: 5px 5px 5px 5px;
                        color: rgb(0, 0, 0);
                        border: 1px solid rgba(246, 183, 118, 0.22) !important;
                    }
                }


                @media (min-width: 577px) and (max-width: 768px) {
                    /* For mobile pad: */
                    .contenedor {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        width: 100%%;
                        height: 100%%;
                        justify-content: center !important;
                    }

                    .logo {
                        padding-top: 58%%;
                        width: 55%%;
                        height: 55%%;
                    }

                    .correcto {
                        font-size: 5vw;
                    }

                    .tex {
                        font-size: 3vw;
                    }

                    .boton {
                        width: 20%%;
                        height: 40px;
                        margin-top: 95px;
                        background-color: rgb(246, 183, 118);
                        border-radius: 5px 5px 5px 5px;
                        color: rgb(0, 0, 0);
                        border: 1px solid rgba(246, 183, 118, 0.22) !important;
                    }
                }
            </style>


            <div class="contenedor">
                <div style="text-align: center;padding-top:5%%">
                    <img class="logo"
                        src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMTIuMSAxMjUuODQiPjxkZWZzPjxzdHlsZT4uY2xzLTF7b3BhY2l0eTowLjg7fS5jbHMtMntmaWxsOiMzNjM2Mzk7fS5jbHMtM3tmaWxsOiNmNmI3NzY7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJDYXBhXzIiIGRhdGEtbmFtZT0iQ2FwYSAyIj48ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIj48ZyBjbGFzcz0iY2xzLTEiPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTE1Ljg4LDEyMS40di01LjI2SDkuNnYtNEgyMC43djEzLjMySDguNzlsLTEtLjE0YTUuNjgsNS42OCwwLDAsMS0xLS4xOWMtLjM2LS4wOS0uODQtLjI1LTEuNDctLjQ4QTguNTEsOC41MSwwLDAsMSwzLDEyMy4xMmE3LjkzLDcuOTMsMCwwLDEtMi4yMi0zLjUxQTE0LjkyLDE0LjkyLDAsMCwxLDAsMTE0LjY3di0xLjM0YTExLjksMTEuOSwwLDAsMSwuMzgtMy4wNywxMi4zMywxMi4zMywwLDAsMSwxLTIuNTksOC44Niw4Ljg2LDAsMCwxLDEuNDgtMi4wOCw5LjQ2LDkuNDYsMCwwLDEsMi41My0xLjc0LDEyLjExLDEyLjExLDAsMCwxLDUuMTgtLjg0SDIwLjd2My45MUgxMC41N2E0Ljk0LDQuOTQsMCwwLDAtMy4yMiwxLDUuMTUsNS4xNSwwLDAsMC0xLjYzLDIuNTgsMTMuMTksMTMuMTksMCwwLDAtLjQ3LDMuNjN2LjM0YTEwLDEwLDAsMCwwLDEuMTEsNS4xM2MuNzQsMS4yMywyLjE1LDEuODUsNC4yMSwxLjg1WiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTI5LjQ5LDEyNS40OUgyNS4xN1YxMDloNy4zMmE2LjIzLDYuMjMsMCwwLDEsMywuNTcsMi40OSwyLjQ5LDAsMCwxLDEuMjgsMS41MywxMCwxMCwwLDAsMSwuMjgsMi42OXYyLjA5SDMyLjkzdi0xLjMxYTYuMDksNi4wOSwwLDAsMC0uMTYtMS43MS45MS45MSwwLDAsMC0uNTktLjU3Yy0uMjcsMC0uNTEtLjA4LS43Mi0uMXMtLjU2LDAtMSwwaC0uOTNaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNTQuNDcsMTIyLjA4djMuNDFINDguMTJxLTQuMjEsMC02LjI3LTIuMjVhOC41OSw4LjU5LDAsMCwxLTItNnEwLTMuNzUsMS41OS01LjUyYTcuMTIsNy4xMiwwLDAsMSwzLjIxLTIuMjQsMTIuNTcsMTIuNTcsMCwwLDEsMy41MS0uNDdoNi4zNXYzLjQxSDQ4LjcyYTguNjgsOC42OCwwLDAsMC0yLjIyLjIyLDIuMiwyLjIsMCwwLDAtMS4yOC45MSwzLjEzLDMuMTMsMCwwLDAtLjU3LDJoOS44MlYxMTlINDQuNjVhMy40MSwzLjQxLDAsMCwwLC40NiwyLDIuMjksMi4yOSwwLDAsMCwxLjI5LjkzLDExLjI5LDExLjI5LDAsMCwwLDIuMjkuMThaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNjIuNTEsMTI1LjQ5SDU4LjE5VjEwOUg3NC44NmExMi45MiwxMi45MiwwLDAsMSwyLjk0LjMyLDUuOTIsNS45MiwwLDAsMSwyLjExLDEsNC40LDQuNCwwLDAsMSwxLjMzLDEuODIsNy42OSw3LjY5LDAsMCwxLC40NywyLjg5djEwLjQ0SDc3LjM2di05Ljg4YTQuNzksNC43OSwwLDAsMC0uMy0xLjkxLDEuNTQsMS41NCwwLDAsMC0xLS44Nyw0Ljc1LDQuNzUsMCwwLDAtMS41My0uMjJINzIuMTF2MTIuODhINjcuNjRWMTEyLjYxSDYyLjUxWiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTg2LjUyLDEwM0g5MXY0LjFoLTQuNVptMCw2SDkxdjE2LjQ4aC00LjVaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNMTA5LjY2LDEyMy41MmE3LjIsNy4yLDAsMCwxLTIuNDQsMS41NSwxMy40NCwxMy40NCwwLDAsMS0yLjA5LjYxLDEwLjA4LDEwLjA4LDAsMCwxLTEuNzUuMTYsMTAuMzYsMTAuMzYsMCwwLDEtMy40NC0uNjEsNy44Nyw3Ljg3LDAsMCwxLTIuODYtMS43MSw2LjU2LDYuNTYsMCwwLDEtMS42NS0yLjM5LDEyLjYsMTIuNiwwLDAsMS0uNjUtMi4xMyw5LDksMCwwLDEtLjE2LTEuNzYsOC4xMyw4LjEzLDAsMCwxLC40OS0zLDExLjMxLDExLjMxLDAsMCwxLC45LTEuODksOS4zMyw5LjMzLDAsMCwxLDEuMzItMS41NSw3LDcsMCwwLDEsMi41My0xLjUsOS45NCw5Ljk0LDAsMCwxLDMuNTItLjYxLDEwLjExLDEwLjExLDAsMCwxLDMuNDIuNTgsNi44LDYuOCwwLDAsMSwyLjU2LDEuNDcsOSw5LDAsMCwxLDEuMzYsMS41Niw5LjczLDkuNzMsMCwwLDEsLjkxLDEuODgsOC42NCw4LjY0LDAsMCwxLC40NywzLjA4LDkuNjcsOS42NywwLDAsMS0uNjEsMy40MkE3Ljg4LDcuODgsMCwwLDEsMTA5LjY2LDEyMy41MlptLTcuNzUtMS41YTIuMjIsMi4yMiwwLDAsMCwuNjQuMTksNSw1LDAsMCwwLC43Ni4wNiw0LjEsNC4xLDAsMCwwLDIuNDQtLjc4LDMuNzQsMy43NCwwLDAsMCwxLjQ2LTEuOTEsNy40NCw3LjQ0LDAsMCwwLC4zNi0yLjI4LDYuNTEsNi41MSwwLDAsMC0uNjEtMi44OSwzLjY1LDMuNjUsMCwwLDAtMi0xLjgsNC42OSw0LjY5LDAsMCwwLTEuNTktLjMxLDQuNTUsNC41NSwwLDAsMC0xLjY5LjM0LDQuNjcsNC42NywwLDAsMC0xLjQxLDEsNC4zOCw0LjM4LDAsMCwwLS44NiwxLjUzLDYuNzQsNi43NCwwLDAsMC0uMywyLjEsNi4xMiw2LjEyLDAsMCwwLC42OCwyLjg4QTMuODUsMy44NSwwLDAsMCwxMDEuOTEsMTIyWiIvPjwvZz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik01Mi43Nyw1MS45MUgzOS42NnY2LjU2SDUyLjc3Vjc4LjY5SDMwLjIxQTEwLjIzLDEwLjIzLDAsMCwxLDIwLDY4LjQ2di0xNkgxMy40M3YxNkExNi44LDE2LjgsMCwwLDAsMzAuMjEsODUuMjRINTkuMzNWNTEuOTFINTIuNzdaIi8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNNzIuNDQsMzkuMzRINjUuODlWNTguNDdoNi41NVY0NS45SDkyLjExVjY4LjQ2QTEwLjIzLDEwLjIzLDAsMCwxLDgxLjg5LDc4LjY5aC0xNnY2LjU1aDE2QTE2LjgsMTYuOCwwLDAsMCw5OC42Nyw2OC40NlYzOS4zNEg3Mi40NFoiLz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik04MS44OSwwSDUyLjc3VjI1LjY4aDB2Ni41Nkg3Mi40NFYyNS42OEg1OS4zM1Y2LjU2SDgxLjg5QTEwLjIzLDEwLjIzLDAsMCwxLDkyLjExLDE2Ljc4VjMyLjUxaDYuNTZWMTYuNzhBMTYuOCwxNi44LDAsMCwwLDgxLjg5LDBaIi8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNMjAsNDUuOUg0Ni4yMVYyNS42OEgzOS42NlYzOS4zNEgyMFYxNi43OEExMC4yMywxMC4yMywwLDAsMSwzMC4yMSw2LjU2aDE2VjBoLTE2QTE2LjgsMTYuOCwwLDAsMCwxMy40MywxNi43OFY0NS45SDIwWiIvPjwvZz48L2c+PC9zdmc+"
                        alt="Img 3" />
                </div>

                <div>
                    <h4 style="text-align: center; " class="correcto"><strong>¡ERROR!</strong></h4>
                    <br>
                    <p style="margin-bottom: 0px;margin-top:-10px; text-align: center;" class="tex">Creación del link</p>
                    <p style="text-align: center;margin-top: -5px;" class="tex">incorrectamente</p>
                </div>

                <button class="boton" onclick="window.location='%s'">SIGUIENTE</button>
            </div>
            """ % old_link
        
    @http.route('/payment/stripe/return', type='http', auth='none')
    def stripe_validate_account_link(self,**kwargs):
        data = kwargs.copy()
        old_link = request.env['res.partner'].sudo().search([('id', '=', data['partner_id'])]).stripe_connect_account_link
        account_verified = request.env['res.partner'].sudo().search([('id', '=', data['partner_id'])]).verify_stripe_connect_account()
        
        if (account_verified):
            return """
          <!DOCTYPE html>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                .contenedor {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%%;
                    height: 100%%;
                    justify-content: center !important;
                }

                .logo {
                    padding-top: 22%%;
                    width: 43%%;
                    height: 43%%;
                }

                .correcto {
                    font-size: 1.8vw;
                    padding-top: 45%%
                }

                .tex {
                    font-size: 1.1vw;
                }

                @media only screen and (max-width: 576px) {

                    /* For mobile phones: */
                    .contenedor {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        width: 100%%;
                        height: 100%%;
                        justify-content: center !important;
                    }

                    .logo {
                        padding-top: 38%%;
                        width: 33%%;
                        height: 33%%;
                    }

                    .correcto {
                        font-size: 5.3vw;
                        margin-bottom: 10px;
                    }

                    .tex {
                        font-size: 3.2vw;
                    }
    
                }


                @media (min-width: 577px) and (max-width: 768px) {
                    /* For mobile pad: */
                    .contenedor {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        width: 100%%;
                        height: 100%%;
                        justify-content: center !important;
                    }

                    .logo {
                        padding-top: 58%%;
                        width: 55%%;
                        height: 55%%;
                    }

                    .correcto {
                        font-size: 5vw;
                    }

                    .tex {
                        font-size: 3vw;
                    }
                  
                }
            </style>


            <div class="contenedor">
                <div style="text-align: center;padding-top:5%%">
                    <img class="logo"
                        src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMTIuMSAxMjUuODQiPjxkZWZzPjxzdHlsZT4uY2xzLTF7b3BhY2l0eTowLjg7fS5jbHMtMntmaWxsOiMzNjM2Mzk7fS5jbHMtM3tmaWxsOiNmNmI3NzY7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJDYXBhXzIiIGRhdGEtbmFtZT0iQ2FwYSAyIj48ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIj48ZyBjbGFzcz0iY2xzLTEiPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTE1Ljg4LDEyMS40di01LjI2SDkuNnYtNEgyMC43djEzLjMySDguNzlsLTEtLjE0YTUuNjgsNS42OCwwLDAsMS0xLS4xOWMtLjM2LS4wOS0uODQtLjI1LTEuNDctLjQ4QTguNTEsOC41MSwwLDAsMSwzLDEyMy4xMmE3LjkzLDcuOTMsMCwwLDEtMi4yMi0zLjUxQTE0LjkyLDE0LjkyLDAsMCwxLDAsMTE0LjY3di0xLjM0YTExLjksMTEuOSwwLDAsMSwuMzgtMy4wNywxMi4zMywxMi4zMywwLDAsMSwxLTIuNTksOC44Niw4Ljg2LDAsMCwxLDEuNDgtMi4wOCw5LjQ2LDkuNDYsMCwwLDEsMi41My0xLjc0LDEyLjExLDEyLjExLDAsMCwxLDUuMTgtLjg0SDIwLjd2My45MUgxMC41N2E0Ljk0LDQuOTQsMCwwLDAtMy4yMiwxLDUuMTUsNS4xNSwwLDAsMC0xLjYzLDIuNTgsMTMuMTksMTMuMTksMCwwLDAtLjQ3LDMuNjN2LjM0YTEwLDEwLDAsMCwwLDEuMTEsNS4xM2MuNzQsMS4yMywyLjE1LDEuODUsNC4yMSwxLjg1WiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTI5LjQ5LDEyNS40OUgyNS4xN1YxMDloNy4zMmE2LjIzLDYuMjMsMCwwLDEsMywuNTcsMi40OSwyLjQ5LDAsMCwxLDEuMjgsMS41MywxMCwxMCwwLDAsMSwuMjgsMi42OXYyLjA5SDMyLjkzdi0xLjMxYTYuMDksNi4wOSwwLDAsMC0uMTYtMS43MS45MS45MSwwLDAsMC0uNTktLjU3Yy0uMjcsMC0uNTEtLjA4LS43Mi0uMXMtLjU2LDAtMSwwaC0uOTNaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNTQuNDcsMTIyLjA4djMuNDFINDguMTJxLTQuMjEsMC02LjI3LTIuMjVhOC41OSw4LjU5LDAsMCwxLTItNnEwLTMuNzUsMS41OS01LjUyYTcuMTIsNy4xMiwwLDAsMSwzLjIxLTIuMjQsMTIuNTcsMTIuNTcsMCwwLDEsMy41MS0uNDdoNi4zNXYzLjQxSDQ4LjcyYTguNjgsOC42OCwwLDAsMC0yLjIyLjIyLDIuMiwyLjIsMCwwLDAtMS4yOC45MSwzLjEzLDMuMTMsMCwwLDAtLjU3LDJoOS44MlYxMTlINDQuNjVhMy40MSwzLjQxLDAsMCwwLC40NiwyLDIuMjksMi4yOSwwLDAsMCwxLjI5LjkzLDExLjI5LDExLjI5LDAsMCwwLDIuMjkuMThaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNjIuNTEsMTI1LjQ5SDU4LjE5VjEwOUg3NC44NmExMi45MiwxMi45MiwwLDAsMSwyLjk0LjMyLDUuOTIsNS45MiwwLDAsMSwyLjExLDEsNC40LDQuNCwwLDAsMSwxLjMzLDEuODIsNy42OSw3LjY5LDAsMCwxLC40NywyLjg5djEwLjQ0SDc3LjM2di05Ljg4YTQuNzksNC43OSwwLDAsMC0uMy0xLjkxLDEuNTQsMS41NCwwLDAsMC0xLS44Nyw0Ljc1LDQuNzUsMCwwLDAtMS41My0uMjJINzIuMTF2MTIuODhINjcuNjRWMTEyLjYxSDYyLjUxWiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTg2LjUyLDEwM0g5MXY0LjFoLTQuNVptMCw2SDkxdjE2LjQ4aC00LjVaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNMTA5LjY2LDEyMy41MmE3LjIsNy4yLDAsMCwxLTIuNDQsMS41NSwxMy40NCwxMy40NCwwLDAsMS0yLjA5LjYxLDEwLjA4LDEwLjA4LDAsMCwxLTEuNzUuMTYsMTAuMzYsMTAuMzYsMCwwLDEtMy40NC0uNjEsNy44Nyw3Ljg3LDAsMCwxLTIuODYtMS43MSw2LjU2LDYuNTYsMCwwLDEtMS42NS0yLjM5LDEyLjYsMTIuNiwwLDAsMS0uNjUtMi4xMyw5LDksMCwwLDEtLjE2LTEuNzYsOC4xMyw4LjEzLDAsMCwxLC40OS0zLDExLjMxLDExLjMxLDAsMCwxLC45LTEuODksOS4zMyw5LjMzLDAsMCwxLDEuMzItMS41NSw3LDcsMCwwLDEsMi41My0xLjUsOS45NCw5Ljk0LDAsMCwxLDMuNTItLjYxLDEwLjExLDEwLjExLDAsMCwxLDMuNDIuNTgsNi44LDYuOCwwLDAsMSwyLjU2LDEuNDcsOSw5LDAsMCwxLDEuMzYsMS41Niw5LjczLDkuNzMsMCwwLDEsLjkxLDEuODgsOC42NCw4LjY0LDAsMCwxLC40NywzLjA4LDkuNjcsOS42NywwLDAsMS0uNjEsMy40MkE3Ljg4LDcuODgsMCwwLDEsMTA5LjY2LDEyMy41MlptLTcuNzUtMS41YTIuMjIsMi4yMiwwLDAsMCwuNjQuMTksNSw1LDAsMCwwLC43Ni4wNiw0LjEsNC4xLDAsMCwwLDIuNDQtLjc4LDMuNzQsMy43NCwwLDAsMCwxLjQ2LTEuOTEsNy40NCw3LjQ0LDAsMCwwLC4zNi0yLjI4LDYuNTEsNi41MSwwLDAsMC0uNjEtMi44OSwzLjY1LDMuNjUsMCwwLDAtMi0xLjgsNC42OSw0LjY5LDAsMCwwLTEuNTktLjMxLDQuNTUsNC41NSwwLDAsMC0xLjY5LjM0LDQuNjcsNC42NywwLDAsMC0xLjQxLDEsNC4zOCw0LjM4LDAsMCwwLS44NiwxLjUzLDYuNzQsNi43NCwwLDAsMC0uMywyLjEsNi4xMiw2LjEyLDAsMCwwLC42OCwyLjg4QTMuODUsMy44NSwwLDAsMCwxMDEuOTEsMTIyWiIvPjwvZz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik01Mi43Nyw1MS45MUgzOS42NnY2LjU2SDUyLjc3Vjc4LjY5SDMwLjIxQTEwLjIzLDEwLjIzLDAsMCwxLDIwLDY4LjQ2di0xNkgxMy40M3YxNkExNi44LDE2LjgsMCwwLDAsMzAuMjEsODUuMjRINTkuMzNWNTEuOTFINTIuNzdaIi8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNNzIuNDQsMzkuMzRINjUuODlWNTguNDdoNi41NVY0NS45SDkyLjExVjY4LjQ2QTEwLjIzLDEwLjIzLDAsMCwxLDgxLjg5LDc4LjY5aC0xNnY2LjU1aDE2QTE2LjgsMTYuOCwwLDAsMCw5OC42Nyw2OC40NlYzOS4zNEg3Mi40NFoiLz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik04MS44OSwwSDUyLjc3VjI1LjY4aDB2Ni41Nkg3Mi40NFYyNS42OEg1OS4zM1Y2LjU2SDgxLjg5QTEwLjIzLDEwLjIzLDAsMCwxLDkyLjExLDE2Ljc4VjMyLjUxaDYuNTZWMTYuNzhBMTYuOCwxNi44LDAsMCwwLDgxLjg5LDBaIi8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNMjAsNDUuOUg0Ni4yMVYyNS42OEgzOS42NlYzOS4zNEgyMFYxNi43OEExMC4yMywxMC4yMywwLDAsMSwzMC4yMSw2LjU2aDE2VjBoLTE2QTE2LjgsMTYuOCwwLDAsMCwxMy40MywxNi43OFY0NS45SDIwWiIvPjwvZz48L2c+PC9zdmc+"
                        alt="Img 3" />
                </div>

                <div>
                    <h4 style="text-align: center; " class="correcto"><strong>¡EXITO!</strong></h4>
                    <br>
                    <p style="margin-bottom: 0px;margin-top:-10px; text-align: center;" class="tex">Su cuenta se ha creado</p>
                    <p style="text-align: center;margin-top: -5px;" class="tex">correctamente</p>
                </div>
            </div>    
                """
        else:
            return """
            <!DOCTYPE html>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                .contenedor {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    width: 100%%;
                    height: 100%%;
                    justify-content: center !important;
                }

                .logo {
                    padding-top: 22%%;
                    width: 43%%;
                    height: 43%%;
                }

                .correcto {
                    font-size: 1.8vw;
                    padding-top: 45%%
                }

                .tex {
                    font-size: 1.1vw;
                }

                .boton {
                    width: 10%%;
                    height: 33px;
                    margin-top: 95px;
                    background-color: rgb(246, 183, 118);
                    border-radius: 5px 5px 5px 5px;
                    color: rgb(0, 0, 0);
                    border: 1px solid rgba(246, 183, 118, 0.22) !important;
                }


                @media only screen and (max-width: 576px) {

                    /* For mobile phones: */
                    .contenedor {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        width: 100%%;
                        height: 100%%;
                        justify-content: center !important;
                    }

                    .logo {
                        padding-top: 38%%;
                        width: 33%%;
                        height: 33%%;
                    }

                    .correcto {
                        font-size: 5.3vw;
                        margin-bottom: 10px;
                    }

                    .tex {
                        font-size: 3.2vw;
                    }

                    .boton {
                        width: 28%%;
                        height: 40px;
                        margin-top: 95px;
                        background-color: rgb(246, 183, 118);
                        border-radius: 5px 5px 5px 5px;
                        color: rgb(0, 0, 0);
                        border: 1px solid rgba(246, 183, 118, 0.22) !important;
                    }
                }


                @media (min-width: 577px) and (max-width: 768px) {
                    /* For mobile pad: */
                    .contenedor {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        width: 100%%;
                        height: 100%%;
                        justify-content: center !important;
                    }

                    .logo {
                        padding-top: 58%%;
                        width: 55%%;
                        height: 55%%;
                    }

                    .correcto {
                        font-size: 5vw;
                    }

                    .tex {
                        font-size: 3vw;
                    }

                    .boton {
                        width: 20%%;
                        height: 40px;
                        margin-top: 95px;
                        background-color: rgb(246, 183, 118);
                        border-radius: 5px 5px 5px 5px;
                        color: rgb(0, 0, 0);
                        border: 1px solid rgba(246, 183, 118, 0.22) !important;
                    }
                }
            </style>


            <div class="contenedor">
                <div style="text-align: center;padding-top:5%%">
                    <img class="logo"
                        src="data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMTIuMSAxMjUuODQiPjxkZWZzPjxzdHlsZT4uY2xzLTF7b3BhY2l0eTowLjg7fS5jbHMtMntmaWxsOiMzNjM2Mzk7fS5jbHMtM3tmaWxsOiNmNmI3NzY7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJDYXBhXzIiIGRhdGEtbmFtZT0iQ2FwYSAyIj48ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIj48ZyBjbGFzcz0iY2xzLTEiPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTE1Ljg4LDEyMS40di01LjI2SDkuNnYtNEgyMC43djEzLjMySDguNzlsLTEtLjE0YTUuNjgsNS42OCwwLDAsMS0xLS4xOWMtLjM2LS4wOS0uODQtLjI1LTEuNDctLjQ4QTguNTEsOC41MSwwLDAsMSwzLDEyMy4xMmE3LjkzLDcuOTMsMCwwLDEtMi4yMi0zLjUxQTE0LjkyLDE0LjkyLDAsMCwxLDAsMTE0LjY3di0xLjM0YTExLjksMTEuOSwwLDAsMSwuMzgtMy4wNywxMi4zMywxMi4zMywwLDAsMSwxLTIuNTksOC44Niw4Ljg2LDAsMCwxLDEuNDgtMi4wOCw5LjQ2LDkuNDYsMCwwLDEsMi41My0xLjc0LDEyLjExLDEyLjExLDAsMCwxLDUuMTgtLjg0SDIwLjd2My45MUgxMC41N2E0Ljk0LDQuOTQsMCwwLDAtMy4yMiwxLDUuMTUsNS4xNSwwLDAsMC0xLjYzLDIuNTgsMTMuMTksMTMuMTksMCwwLDAtLjQ3LDMuNjN2LjM0YTEwLDEwLDAsMCwwLDEuMTEsNS4xM2MuNzQsMS4yMywyLjE1LDEuODUsNC4yMSwxLjg1WiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTI5LjQ5LDEyNS40OUgyNS4xN1YxMDloNy4zMmE2LjIzLDYuMjMsMCwwLDEsMywuNTcsMi40OSwyLjQ5LDAsMCwxLDEuMjgsMS41MywxMCwxMCwwLDAsMSwuMjgsMi42OXYyLjA5SDMyLjkzdi0xLjMxYTYuMDksNi4wOSwwLDAsMC0uMTYtMS43MS45MS45MSwwLDAsMC0uNTktLjU3Yy0uMjcsMC0uNTEtLjA4LS43Mi0uMXMtLjU2LDAtMSwwaC0uOTNaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNTQuNDcsMTIyLjA4djMuNDFINDguMTJxLTQuMjEsMC02LjI3LTIuMjVhOC41OSw4LjU5LDAsMCwxLTItNnEwLTMuNzUsMS41OS01LjUyYTcuMTIsNy4xMiwwLDAsMSwzLjIxLTIuMjQsMTIuNTcsMTIuNTcsMCwwLDEsMy41MS0uNDdoNi4zNXYzLjQxSDQ4LjcyYTguNjgsOC42OCwwLDAsMC0yLjIyLjIyLDIuMiwyLjIsMCwwLDAtMS4yOC45MSwzLjEzLDMuMTMsMCwwLDAtLjU3LDJoOS44MlYxMTlINDQuNjVhMy40MSwzLjQxLDAsMCwwLC40NiwyLDIuMjksMi4yOSwwLDAsMCwxLjI5LjkzLDExLjI5LDExLjI5LDAsMCwwLDIuMjkuMThaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNjIuNTEsMTI1LjQ5SDU4LjE5VjEwOUg3NC44NmExMi45MiwxMi45MiwwLDAsMSwyLjk0LjMyLDUuOTIsNS45MiwwLDAsMSwyLjExLDEsNC40LDQuNCwwLDAsMSwxLjMzLDEuODIsNy42OSw3LjY5LDAsMCwxLC40NywyLjg5djEwLjQ0SDc3LjM2di05Ljg4YTQuNzksNC43OSwwLDAsMC0uMy0xLjkxLDEuNTQsMS41NCwwLDAsMC0xLS44Nyw0Ljc1LDQuNzUsMCwwLDAtMS41My0uMjJINzIuMTF2MTIuODhINjcuNjRWMTEyLjYxSDYyLjUxWiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTg2LjUyLDEwM0g5MXY0LjFoLTQuNVptMCw2SDkxdjE2LjQ4aC00LjVaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNMTA5LjY2LDEyMy41MmE3LjIsNy4yLDAsMCwxLTIuNDQsMS41NSwxMy40NCwxMy40NCwwLDAsMS0yLjA5LjYxLDEwLjA4LDEwLjA4LDAsMCwxLTEuNzUuMTYsMTAuMzYsMTAuMzYsMCwwLDEtMy40NC0uNjEsNy44Nyw3Ljg3LDAsMCwxLTIuODYtMS43MSw2LjU2LDYuNTYsMCwwLDEtMS42NS0yLjM5LDEyLjYsMTIuNiwwLDAsMS0uNjUtMi4xMyw5LDksMCwwLDEtLjE2LTEuNzYsOC4xMyw4LjEzLDAsMCwxLC40OS0zLDExLjMxLDExLjMxLDAsMCwxLC45LTEuODksOS4zMyw5LjMzLDAsMCwxLDEuMzItMS41NSw3LDcsMCwwLDEsMi41My0xLjUsOS45NCw5Ljk0LDAsMCwxLDMuNTItLjYxLDEwLjExLDEwLjExLDAsMCwxLDMuNDIuNTgsNi44LDYuOCwwLDAsMSwyLjU2LDEuNDcsOSw5LDAsMCwxLDEuMzYsMS41Niw5LjczLDkuNzMsMCwwLDEsLjkxLDEuODgsOC42NCw4LjY0LDAsMCwxLC40NywzLjA4LDkuNjcsOS42NywwLDAsMS0uNjEsMy40MkE3Ljg4LDcuODgsMCwwLDEsMTA5LjY2LDEyMy41MlptLTcuNzUtMS41YTIuMjIsMi4yMiwwLDAsMCwuNjQuMTksNSw1LDAsMCwwLC43Ni4wNiw0LjEsNC4xLDAsMCwwLDIuNDQtLjc4LDMuNzQsMy43NCwwLDAsMCwxLjQ2LTEuOTEsNy40NCw3LjQ0LDAsMCwwLC4zNi0yLjI4LDYuNTEsNi41MSwwLDAsMC0uNjEtMi44OSwzLjY1LDMuNjUsMCwwLDAtMi0xLjgsNC42OSw0LjY5LDAsMCwwLTEuNTktLjMxLDQuNTUsNC41NSwwLDAsMC0xLjY5LjM0LDQuNjcsNC42NywwLDAsMC0xLjQxLDEsNC4zOCw0LjM4LDAsMCwwLS44NiwxLjUzLDYuNzQsNi43NCwwLDAsMC0uMywyLjEsNi4xMiw2LjEyLDAsMCwwLC42OCwyLjg4QTMuODUsMy44NSwwLDAsMCwxMDEuOTEsMTIyWiIvPjwvZz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik01Mi43Nyw1MS45MUgzOS42NnY2LjU2SDUyLjc3Vjc4LjY5SDMwLjIxQTEwLjIzLDEwLjIzLDAsMCwxLDIwLDY4LjQ2di0xNkgxMy40M3YxNkExNi44LDE2LjgsMCwwLDAsMzAuMjEsODUuMjRINTkuMzNWNTEuOTFINTIuNzdaIi8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNNzIuNDQsMzkuMzRINjUuODlWNTguNDdoNi41NVY0NS45SDkyLjExVjY4LjQ2QTEwLjIzLDEwLjIzLDAsMCwxLDgxLjg5LDc4LjY5aC0xNnY2LjU1aDE2QTE2LjgsMTYuOCwwLDAsMCw5OC42Nyw2OC40NlYzOS4zNEg3Mi40NFoiLz48cGF0aCBjbGFzcz0iY2xzLTMiIGQ9Ik04MS44OSwwSDUyLjc3VjI1LjY4aDB2Ni41Nkg3Mi40NFYyNS42OEg1OS4zM1Y2LjU2SDgxLjg5QTEwLjIzLDEwLjIzLDAsMCwxLDkyLjExLDE2Ljc4VjMyLjUxaDYuNTZWMTYuNzhBMTYuOCwxNi44LDAsMCwwLDgxLjg5LDBaIi8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNMjAsNDUuOUg0Ni4yMVYyNS42OEgzOS42NlYzOS4zNEgyMFYxNi43OEExMC4yMywxMC4yMywwLDAsMSwzMC4yMSw2LjU2aDE2VjBoLTE2QTE2LjgsMTYuOCwwLDAsMCwxMy40MywxNi43OFY0NS45SDIwWiIvPjwvZz48L2c+PC9zdmc+"
                        alt="Img 3" />
                </div>

                <div>
                    <h4 style="text-align: center; " class="correcto"><strong>¡ERROR!</strong></h4>
                    <br>
                    <p style="margin-bottom: 0px;margin-top:-10px; text-align: center;" class="tex">Creacion de cuenta</p>
                    <p style="text-align: center;margin-top: -5px;" class="tex">incompleta</p>
                </div>

                <button class="boton" onclick="window.location='%s'">COMPLETAR</button>
            </div>
            """ % old_link
     
